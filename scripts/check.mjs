import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve('dist');let checked=0;const failures=[];
function walk(folder){return fs.readdirSync(folder,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(folder,e.name)):[path.join(folder,e.name)]);}
for(const file of walk(root).filter(x=>x.endsWith('.html'))){checked++;const html=fs.readFileSync(file,'utf8');for(const match of html.matchAll(/(?:href|src)="([^"]+)"/g)){let url=match[1].replace(/&amp;/g,'&');if(/^(https?:|data:|mailto:|#)/.test(url))continue;url=url.split('#')[0].split('?')[0];if(!url)continue;let target=path.resolve(url.startsWith('/')?root:path.dirname(file),url.startsWith('/')?'.'+decodeURIComponent(url):decodeURIComponent(url));if(fs.existsSync(target)&&fs.statSync(target).isDirectory())target=path.join(target,'index.html');if(!fs.existsSync(target))failures.push(`${path.relative(root,file)}: missing ${url}`);}if(!/<title>.+<\/title>/.test(html))failures.push(`${file}: no title`);}
const index=JSON.parse(fs.readFileSync(path.join(root,'search-index.json'),'utf8'));if(!index.some(x=>x.title.includes('同步 DC-DC Buck')))failures.push('Chinese search index missing learning topics');if(!index.some(x=>x.title==='IC Schematics Studio'))failures.push('Project missing from search index');
if(failures.length){console.error(failures.join('\n'));process.exitCode=1;}else console.log(`Checked ${checked} HTML files: local routes and assets resolve; Chinese search index present.`);

