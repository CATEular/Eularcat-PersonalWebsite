import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import matter from 'gray-matter';
import {Cite} from '@citation-js/core';
import '@citation-js/plugin-bibtex';
export function slugify(text){return String(text).normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{N}]+/gu,'-').replace(/^-|-$/g,'')||'note';}
function nameOf(author){return typeof author==='string'?author:author.literal||[author.given,author.family].filter(Boolean).join(' ');}
function normalizeCitation(x){return {key:String(x.id||''),title:x.title||'',authors:(x.author||[]).map(nameOf),year:x.issued?.['date-parts']?.[0]?.[0]||null,venue:x['container-title']||x.publisher||'',doi:x.DOI||'',url:x.URL||'',tags:Array.isArray(x.keyword)?x.keyword:String(x.keyword||'').split(/[,;]/).map(s=>s.trim()).filter(Boolean)};}
export function parseRIS(text){const entries=[];let record={},last;
 const listTags=new Set(['AU','A1','KW']);
 for(const line of text.replace(/\r/g,'').split('\n')){const match=line.match(/^([A-Z0-9]{2})\s{2}-\s?(.*)$/);if(match){const [,tag,value]=match;if(tag==='TY'){record={};last=null;}else if(tag==='ER'){if(Object.keys(record).length)entries.push({key:record.ID||'',title:record.TI||record.T1||'',authors:record.AU||record.A1||[],year:Number((record.PY||record.Y1||'').match(/\d{4}/)?.[0])||null,venue:record.JO||record.JF||record.T2||record.PB||'',doi:record.DO||'',url:record.UR||'',tags:record.KW||[]});record={};last=null;}else{if(listTags.has(tag)){(record[tag]??=[]).push(value);}else record[tag]=value;last=tag;}}else if(line.trim()&&last){if(Array.isArray(record[last]))record[last][record[last].length-1]+=' '+line.trim();else record[last]+=' '+line.trim();}}
 if(Object.keys(record).length)throw new Error('RIS entry is missing its ER end marker.');return entries;
}
export function readBibliography(file,key){const ext=path.extname(file).toLowerCase(),raw=fs.readFileSync(file,'utf8');let entries;
 if(ext==='.ris')entries=parseRIS(raw);else if(ext==='.bib')entries=new Cite(raw).data.map(normalizeCitation);else if(ext==='.json'){const data=JSON.parse(raw);entries=(Array.isArray(data)?data:[data]).map(normalizeCitation);}else throw new Error('Bibliography must be .bib, .ris or CSL .json.');
 if(!entries.length)throw new Error('No bibliography entries found.');if(key){const item=entries.find(x=>x.key===key);if(!item)throw new Error(`Bibliography key not found: ${key}`);return item;}if(entries.length!==1)throw new Error('Multiple bibliography entries found. Select one with --key.');return entries[0];
}
function findFiles(folder){if(!fs.existsSync(folder))return [];const found=[];for(const e of fs.readdirSync(folder,{withFileTypes:true})){const f=path.join(folder,e.name);if(e.isDirectory())found.push(...findFiles(f));else if(e.isFile())found.push(f);}return found;}
export function importContent({note,bibliography,assets,slug,type='notes',key,root=process.cwd()}){
 if(!['notes','reading','learn'].includes(type))throw new Error('Type must be notes, reading or learn.');if(!note)throw new Error('A Markdown note is required (--note).');note=path.resolve(note);if(!fs.existsSync(note))throw new Error(`Note not found: ${note}`);
 const parsed=matter(fs.readFileSync(note,'utf8')),citation=bibliography?readBibliography(path.resolve(bibliography),key):{};
 if(type==='reading'&&!bibliography&&!parsed.data.title)throw new Error('Paper import requires bibliography metadata or a title in Markdown frontmatter.');
 const title=parsed.data.title||citation.title||path.basename(note,path.extname(note));slug=slug||slugify(title);
 if(!/^[\p{L}\p{N}][\p{L}\p{N}-]*$/u.test(slug))throw new Error('Slug must contain only letters, numbers and hyphens.');
 const lang=parsed.data.lang||'zh';if(!['zh','en'].includes(lang))throw new Error('Note language must be zh or en.');const status=parsed.data.status||'draft';if(!['planned','learning','draft','published'].includes(status))throw new Error('Invalid content status. Use planned, learning, draft or published.');
 const dest=path.resolve(root,'content',type,slug);if(fs.existsSync(dest))throw new Error(`Content already exists; import will not overwrite it: ${dest}`);
 const sourceRoot=path.dirname(note),assetRoot=assets?path.resolve(assets):sourceRoot,assetFiles=findFiles(assetRoot),copies=new Map(),names=new Map();
 function resolveAsset(ref){let clean;try{clean=decodeURIComponent(ref.split('#')[0]);}catch{clean=ref;}clean=clean.replace(/\\/g,'/');const direct=[path.resolve(sourceRoot,clean),path.resolve(assetRoot,clean)];let matches=direct.filter(f=>fs.existsSync(f)&&fs.statSync(f).isFile());if(!matches.length)matches=assetFiles.filter(f=>f.replace(/\\/g,'/').endsWith('/'+clean)||path.basename(f)===path.basename(clean));matches=[...new Set(matches)];if(matches.length!==1)throw new Error(matches.length?`Ambiguous asset reference: ${ref}. Use a relative path.`:`Missing asset: ${ref}`);
 const original=matches[0],filename=path.basename(original);if(names.has(filename)&&names.get(filename)!==original)throw new Error(`Two assets have the same filename: ${filename}`);names.set(filename,original);copies.set(original,filename);return './assets/'+encodeURIComponent(filename);
 }
 let body=parsed.content.replace(/!\[\[([^\]]+)\]\]/g,(_,ref)=>{const file=ref.split('|')[0].trim();return `![${path.basename(file,path.extname(file)).replace(/[\[\]]/g,'')}](${resolveAsset(file)})`;});
 body=body.replace(/(!\[[^\]]*\]\()(<[^>]+>|(?:\\.|[^\s)])+)(\s+(?:"[^"]*"|'[^']*')\s*)?\)/g,(_,prefix,target,title='')=>{const ref=target.startsWith('<')?target.slice(1,-1):target;if(/^(https?:|data:|\/\/)/i.test(ref)||ref.startsWith('./assets/')&&[...copies.values()].some(n=>'./assets/'+encodeURIComponent(n)===ref))return prefix+target+title+')';return prefix+resolveAsset(ref)+title+')';});
 // Obsidian callouts retain their quoted structure and become readable Markdown.
 body=body.replace(/^>\s*\[!([^\]]+)\][+-]?\s*(.*)$/gm,(_,kind,label)=>`> **${label||kind}**`);
 const metadata={...citation,...parsed.data,title,lang,type:type==='notes'?'note':type==='reading'?'reading':'learn',status};delete metadata.key;
 fs.mkdirSync(path.join(dest,'assets'),{recursive:true});try{for(const [source,name]of copies)fs.copyFileSync(source,path.join(dest,'assets',name));const filename=type==='reading'?'note.md':'index.md';fs.writeFileSync(path.join(dest,filename),matter.stringify(body,metadata));if(type==='reading')fs.writeFileSync(path.join(dest,'metadata.yaml'),JSON.stringify(metadata,null,2)+'\n');}catch(error){throw new Error(`Import could not finish at ${dest}: ${error.message}`);}
 return {directory:dest,slug,lang,status,assets:copies.size,title};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const args=process.argv.slice(2);if(args.includes('--help')){console.log('npm run import -- --note <note.md> [--type notes|reading|learn] [--bibliography <.bib|.ris|.json>] [--key <citation-key>] [--assets <folder>] [--slug <slug>]\nNotes keep their original language. Missing assets fail the import. Existing content is never overwritten. Default status: draft.');}else{try{const options={};for(let i=0;i<args.length;i+=2){const name=args[i].replace(/^--/,'');if(!['note','type','bibliography','assets','slug','key'].includes(name)||!args[i+1])throw new Error(`Unknown or incomplete argument: ${args[i]}`);options[name]=args[i+1];}console.log(JSON.stringify(importContent(options),null,2));}catch(e){console.error('Import failed: '+e.message);process.exitCode=1;}}
}
