import argparse, hashlib, json, pathlib, re, shutil, sqlite3, tempfile

def locate():
    root = pathlib.Path.home() / 'AppData/Roaming/Zotero/Zotero/Profiles'
    dirs = set()
    for p in root.glob('*/prefs.js'):
        m = re.search(r'user_pref\("extensions.zotero.dataDir",\s*("(?:[^"\\]|\\.)*")\)', p.read_text(encoding='utf-8'))
        if m:
            dirs.add(json.loads(m.group(1)))
    if len(dirs) != 1:
        raise RuntimeError('Expected one configured Zotero data directory; specify --data-dir')
    return pathlib.Path(dirs.pop())

def signature(paths):
    return [(p.name, p.stat().st_size, p.stat().st_mtime_ns) for p in paths if p.exists()]

def main():
    a = argparse.ArgumentParser()
    g = a.add_mutually_exclusive_group(required=True)
    g.add_argument('--query'); g.add_argument('--item-key')
    a.add_argument('--out', required=True); a.add_argument('--data-dir'); a.add_argument('--linked-base')
    args = a.parse_args()
    data = pathlib.Path(args.data_dir) if args.data_dir else locate()
    source = data / 'zotero.sqlite'
    if not source.is_file(): raise RuntimeError('Database missing')
    files = [source, pathlib.Path(str(source)+'-wal'), pathlib.Path(str(source)+'-shm')]
    with tempfile.TemporaryDirectory(prefix='zotero-read-') as td:
        before = signature(files)
        for p in files:
            if p.exists(): shutil.copy2(p, pathlib.Path(td) / p.name)
        if before != signature(files): raise RuntimeError('Source changed during snapshot; retry later')
        con = sqlite3.connect((pathlib.Path(td)/source.name).as_uri()+'?mode=ro', uri=True)
        con.row_factory = sqlite3.Row
        if con.execute('PRAGMA quick_check').fetchone()[0] != 'ok': raise RuntimeError('Invalid snapshot')
        rows = [dict(r) for r in con.execute('''SELECT i.itemID,i.key,v.value title FROM items i JOIN itemData d USING(itemID) JOIN fields f USING(fieldID) JOIN itemDataValues v USING(valueID) WHERE f.fieldName='title' AND i.itemID NOT IN (SELECT itemID FROM deletedItems) AND i.itemID NOT IN (SELECT itemID FROM itemAttachments) AND i.itemID NOT IN (SELECT itemID FROM itemNotes)''')]
        matches = [r for r in rows if (r['key']==args.item_key if args.item_key else args.query.casefold() in r['title'].casefold())]
        result = {'status':'ambiguous' if len(matches)>1 else 'not_found', 'candidates':[{'key':r['key'],'title':r['title']} for r in matches]}
        if len(matches)==1:
            p = matches[0]
            meta = dict(con.execute('SELECT f.fieldName,v.value FROM itemData d JOIN fields f USING(fieldID) JOIN itemDataValues v USING(valueID) WHERE d.itemID=?',(p['itemID'],)))
            creators = [dict(r) for r in con.execute('SELECT c.firstName,c.lastName,ic.orderIndex FROM itemCreators ic JOIN creators c USING(creatorID) WHERE ic.itemID=? ORDER BY ic.orderIndex',(p['itemID'],))]
            attachments = []
            for r in con.execute('SELECT i.itemID,i.key,a.path,a.contentType FROM itemAttachments a JOIN items i USING(itemID) WHERE a.parentItemID=? AND i.itemID NOT IN (SELECT itemID FROM deletedItems)',(p['itemID'],)):
                att = dict(r); path = att['path'] or ''
                resolved = data/'storage'/att['key']/path[8:] if path.startswith('storage:') else pathlib.Path(args.linked_base)/path[12:] if path.startswith('attachments:') and args.linked_base else pathlib.Path(path) if path and not path.startswith('attachments:') else None
                att['resolvedPath'] = str(resolved) if resolved else None
                att['fileExists'] = bool(resolved and resolved.is_file())
                annotations = []
                for ar in con.execute('SELECT i.key annotationKey,a.* FROM itemAnnotations a JOIN items i USING(itemID) WHERE a.parentItemID=? AND i.itemID NOT IN (SELECT itemID FROM deletedItems)',(att['itemID'],)):
                    ann = dict(ar)
                    if ann.get('position'):
                        ann['position'] = json.loads(ann['position'])
                    payload = {k:ann.get(k) for k in ('text','comment','color','position','type','pageLabel')}
                    ann['contentHash'] = hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
                    annotations.append(ann)
                att['annotations'] = annotations; attachments.append(att)
            result = {'status':'unique','paperKey':p['key'],'metadata':meta,'creators':creators,'attachments':attachments}
        con.close()
    out = pathlib.Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'status':result['status'],'candidateCount':len(matches),'annotationCount':sum(len(x['annotations']) for x in result.get('attachments',[]))}))
if __name__ == '__main__': main()
