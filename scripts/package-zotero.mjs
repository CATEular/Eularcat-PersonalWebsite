import fs from 'node:fs';
import path from 'node:path';
import {zipSync} from 'fflate';
export const zoteroFiles=['SKILL.md','config.example.json','references/preferences.md','references/local-reading.md','scripts/read_paper.py'];
export function packageZotero(root,out){
 const files={};
 for(const name of zoteroFiles){
  const bytes=fs.readFileSync(path.join(root,'skills','zotero-reading-notes',name));
  const text=bytes.toString('utf8').replaceAll('http://127.0.0.1:23119/api/users/0','');
  if(/(?:\b[A-Za-z]:[\\/]|\/Users\/|\/home\/[^/\s]+\/)/i.test(text))throw new Error('Personal path in skill export: '+name);
  files['zotero-reading-notes/'+name]=new Uint8Array(bytes);
 }
 for(const [name,bytes] of Object.entries(files)){
  const target=path.join(out,'downloads',name);fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,bytes);
 }
 fs.writeFileSync(path.join(out,'downloads','zotero-reading-notes.zip'),zipSync(files,{level:6}));
}
