import fs from 'node:fs';
import path from 'node:path';
import {zipSync} from 'fflate';

export function packageVirtuoso(root,out){
 const source=path.join(root,'skills','virtuoso-workflow');
 const names=JSON.parse(fs.readFileSync(path.join(source,'export-manifest.json'),'utf8'));
 if(!Array.isArray(names)||new Set(names).size!==names.length)throw new Error('Invalid Virtuoso export manifest');
 const forbiddenFile=/(?:^|\/)(?:agents|\.agents|\.codex|\.openai|validation|__pycache__)(?:\/|$)|(?:config\.local\.json|\.env|AGENTS\.md|CLAUDE\.md|\.pyc|\.log|\.pdf|\.zip)$/i;
 const forbiddenText=/(?:\b[A-Z]:[\\/]|\/Users\/|\/home\/[^/\s]+\/|192\.168\.\d+\.\d+|github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,}|BEGIN [A-Z ]*PRIVATE KEY)/i;
 const files={},mtime=new Date('2026-10-08T00:00:00Z');
 for(const name of [...names,'export-manifest.json']){
  if(typeof name!=='string'||name.startsWith('/')||name.includes('\\')||name.split('/').includes('..')||forbiddenFile.test(name))throw new Error('Forbidden Virtuoso export path: '+name);
  const filename=path.join(source,name);
  if(fs.lstatSync(filename).isSymbolicLink())throw new Error('Symlink in Virtuoso export: '+name);
  const text=fs.readFileSync(filename,'utf8').replace(/\r\n/g,'\n'),bytes=Buffer.from(text,'utf8');
  if(forbiddenText.test(text))throw new Error('Private information in Virtuoso export: '+name);
  if(name.endsWith('.md'))for(const match of text.matchAll(/\]\(([^)]+)\)/g)){
   const href=match[1].split('#')[0];
   if(!href||/^(https?:|<|\$)/.test(href))continue;
   const ref=path.relative(source,path.resolve(path.dirname(filename),href)).replaceAll('\\','/');
   if(![...names,'export-manifest.json'].includes(ref))throw new Error('Unpackaged reference: '+name+' -> '+href);
  }
  files['virtuoso-workflow/'+name]=[new Uint8Array(bytes),{mtime}];
  const target=path.join(out,'downloads','virtuoso-workflow',name);
  fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,bytes);
 }
 const archive=zipSync(files,{level:6,mtime});
 fs.writeFileSync(path.join(out,'downloads','virtuoso-workflow.zip'),archive);
 return {files:names.length+1,bytes:archive.length};
}
