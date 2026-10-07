import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';
import {renderMarkdown} from './markdown.mjs';
export {renderMarkdown} from './markdown.mjs';
export function loadContent(root){const items=[];
 for(const type of ['notes','reading','learn']){const folder=path.join(root,'content',type);if(!fs.existsSync(folder))continue;
  for(const entry of fs.readdirSync(folder,{withFileTypes:true})){if(!entry.isDirectory())continue;const dir=path.join(folder,entry.name),file=path.join(dir,type==='reading'?'note.md':'index.md');if(!fs.existsSync(file))continue;
   const parsed=matter(fs.readFileSync(file,'utf8'));let metadata={};if(type==='reading'&&fs.existsSync(path.join(dir,'metadata.yaml')))metadata=matter('---\n'+fs.readFileSync(path.join(dir,'metadata.yaml'),'utf8')+'\n---').data;
   const data={...metadata,...parsed.data};if(data.status!=='published')continue;if(!data.title)throw new Error(`Missing title: ${file}`);if(!['zh','en'].includes(data.lang))throw new Error(`lang must be zh or en: ${file}`);
   const rendered=renderMarkdown(parsed.content);const words=parsed.content.match(/[\p{Script=Han}]|[\p{L}\p{N}]+/gu)||[];
   items.push({...data,type,slug:entry.name,dir,source:parsed.content,...rendered,readingTime:Math.max(1,Math.ceil(words.length/300)),date:normalizeDate(data.date),updated:normalizeDate(data.updated||data.date)});
  }
 }
 return items.sort((a,b)=>(b.date||'').localeCompare(a.date||''));
}
function normalizeDate(value){if(!value)return '';if(value instanceof Date)return value.toISOString().slice(0,10);return String(value).slice(0,10);}
