import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import matter from 'gray-matter';
import {importContent} from './index.mjs';

// Normalize a copy for the website; never rewrite the user's vault note.
export function normalizePaper(source,{publish=false,description}={}){
 const parsed=matter(source),original=parsed.data;
 const authors=Array.isArray(original.authors)?original.authors:String(original.authors||'').split(/[,;；]/).map(x=>x.trim()).filter(Boolean);
 const date=x=>x instanceof Date?x.toISOString().slice(0,10):x;
 const year=String(original.year||original.published||'').match(/\b\d{4}\b/)?.[0];
 const metadata={...original,title:original.title,authors,lang:original.lang||'zh',venue:original.venue||original.publication||'',year:year?Number(year):null,date:date(original.date||original.created),updated:date(original.updated),status:publish?'published':'draft'};
 if(description)metadata.description=description;
 const url=original.url||original.source_url;
 if(url&&/^https?:\/\//i.test(url))metadata.url=url;else delete metadata.url;
 for(const key of ['publication','published','created','source_url'])delete metadata[key];
 for(const key of Object.keys(metadata))if(metadata[key]===undefined)delete metadata[key];
 // The page heading already shows the note title. Unpublished wiki targets stay
 // readable as labels, rather than linking to nonexistent website pages.
 let body=parsed.content.replace(/^\s*# [^\n]+\n/, '\n');
 body=body.split(/(```[^\n]*\n[\s\S]*?```|~~~[^\n]*\n[\s\S]*?~~~)/g).map((part,i)=>i%2?part:part.replace(/(?<!!)\[\[([\s\S]*?)\]\]/g,(_,link)=>{const bar=link.indexOf('|');return bar<0?link:link.slice(bar+1);})).join('');
 return matter.stringify(body,metadata);
}

export function importObsidianPaper({note,assets,slug,publish=false,description,root=process.cwd()}){
 if(!note)throw new Error('A source Markdown note is required (--note).');
 const source=path.resolve(note),temp=fs.mkdtempSync(path.join(os.tmpdir(),'eularcat-paper-'));
 try{
  const staged=path.join(temp,'note.md');
  fs.writeFileSync(staged,normalizePaper(fs.readFileSync(source,'utf8'),{publish,description}));
  return importContent({note:staged,assets:assets||path.dirname(source),slug,type:'reading',root});
 }finally{fs.rmSync(temp,{recursive:true,force:true});}
}

if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const args=process.argv.slice(2);
 if(args.includes('--help'))console.log('npm run import:paper -- --note <Obsidian paper.md> --slug <slug> [--assets <specific image folder>] [--description <summary>] [--publish]\nOriginal vault files are never modified. Default: draft. Explicit --publish makes the imported copy public after deployment.');
 else try{
  const options={};
  for(let i=0;i<args.length;i++){const name=args[i].replace(/^--/,'');if(name==='publish')options.publish=true;else if(['note','assets','slug','description'].includes(name)&&args[i+1]&&!args[i+1].startsWith('--'))options[name]=args[++i];else throw new Error('Unknown or incomplete argument: '+args[i]);}
  console.log(JSON.stringify(importObsidianPaper(options),null,2));
 }catch(error){console.error('Paper import failed: '+error.message);process.exitCode=1;}
}
