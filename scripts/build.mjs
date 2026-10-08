import fs from 'node:fs';
import path from 'node:path';
import {copy,routes,topicZh} from '../src/i18n/index.mjs';
import {layout,escape,pageHeader} from '../src/components/layout.mjs';
import {home} from '../src/components/home.mjs';
import * as pages from '../src/components/pages.mjs';
import {articlesForTopic,articlePath} from '../src/learning.mjs';
import {loadContent} from '../src/content.mjs';
import matter from 'gray-matter';
import {renderMarkdown} from '../src/markdown.mjs';
import {packageSkill} from './package-skill.mjs';
const root=process.cwd(),out=path.join(root,'dist'),site=JSON.parse(fs.readFileSync('content/site.json','utf8'));
const aiContent=JSON.parse(fs.readFileSync('content/ai-ic.json','utf8'));
const origin=process.env.SITE_ORIGIN||site.origin||'http://localhost:4321';
const items=loadContent(root), urls=[],search=[];
// Recreate only this project's generated output so unpublished or removed notes cannot remain live.
if(out!==path.resolve(root,'dist'))throw new Error('Invalid output directory');
fs.rmSync(out,{recursive:true,force:true});
fs.mkdirSync(out,{recursive:true});fs.cpSync('public',out,{recursive:true});fs.mkdirSync(path.join(out,'assets'),{recursive:true});fs.copyFileSync('src/styles/site.css',path.join(out,'assets/site.css'));fs.cpSync('node_modules/katex/dist',path.join(out,'assets/katex'),{recursive:true});
fs.writeFileSync(path.join(out,'assets/highlight.css'),fs.readFileSync('node_modules/highlight.js/styles/github.css','utf8')+'\n'+fs.readFileSync('node_modules/highlight.js/styles/github-dark.css','utf8').replace(/\.hljs/g,'[data-theme="dark"] .hljs'));
packageSkill(root,out);
const about={},skillDocuments={};
for(const lang of ['zh','en']){const source=fs.readFileSync(`content/about/${lang}.md`,'utf8'),doc=matter(source);about[lang]={...doc.data,...renderMarkdown(doc.content)};const skill=matter(fs.readFileSync(`content/skills/analog-ic-notes/${lang}.md`,'utf8'));skillDocuments[lang]={...skill.data,...renderMarkdown(skill.content)};}
function write(route,html){const target=path.join(out,route,'index.html');fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,html);}
function emit(lang,route,title,description,body,extra={}){const pathname=`/${lang}/${route}${route?'/':''}`;write(pathname,layout({lang,route,title,description,body,origin,...extra}));urls.push({path:pathname,lang,alternate:extra.alternate!==false});}
for(const lang of ['zh','en']){const t=copy[lang];emit(lang,'',lang==='zh'?'模拟集成电路设计，借助 AI':'Analog IC Design, augmented by AI',t.intro,home(lang,site,items));
 emit(lang,'learn',t.learning,t.learnPageIntro,pages.learn(lang,site,items));emit(lang,'reading',t.nav[1],t.readingIntro,pages.library(lang,'reading',items));emit(lang,'ai-ic','AI × IC',t.aiIntro,pages.ai(lang,aiContent,items));emit(lang,'ai-ic/analog-ic-notes','Analog IC Notes',skillDocuments[lang].description,pages.skillPage(lang,skillDocuments[lang]),{article:true});emit(lang,'projects',t.nav[3],t.projectIntro,pages.projects(lang,site));emit(lang,'notes',t.nav[4],t.notesIntro,pages.library(lang,'notes',items));emit(lang,'about','Eularcat',t.aboutIntro,pages.about(lang,about[lang]),{article:true});emit(lang,'projects/ic-schematics-studio','IC Schematics Studio',t.studioSummary,pages.studio(lang,site));emit(lang,'search',t.search,t.searchStart,pages.searchPage(lang));
 search.push({title:'Analog IC Notes',description:skillDocuments[lang].description,text:'skill 模拟 IC 论文笔记 Markdown Obsidian',type:'ai-ic',lang,url:`/${lang}/ai-ic/analog-ic-notes/`});
 for(const [i,r] of routes.entries())search.push({title:t.nav[i],description:[t.learnPageIntro,t.readingIntro,t.aiIntro,t.projectIntro,t.notesIntro,t.aboutIntro][i],text:t.nav[i],type:r,lang,url:`/${lang}/${r}/`});search.push({title:'IC Schematics Studio',description:t.studioSummary,text:'IC 原理图 绘图 Schematic browser web tool',type:'projects',lang,url:`/${lang}/projects/ic-schematics-studio/`});
 for(const group of site.learning)for(const topic of group.topics){const records=articlesForTopic(items,topic),article=records[0];search.push({title:lang==='zh'?topicZh[topic]||topic:topic,description:article?article.description||article.title:t.planned+' · '+t.unpublished,text:topic+' '+(topicZh[topic]||''),type:'learn',lang,url:article?articlePath(article):`/${lang}/learn/#${topic.toLowerCase().replace(/[^a-z0-9]+/g,'-')}`,status:article?'published':'planned'});}
}
for(const item of items){emit(item.lang,`${item.type}/${item.slug}`,item.title,item.description||'',pages.article(item),{article:true,alternate:false});const target=path.join(out,item.lang,item.type,item.slug,'assets');if(fs.existsSync(path.join(item.dir,'assets')))fs.cpSync(path.join(item.dir,'assets'),target,{recursive:true});search.push({title:item.title,description:item.description||'',text:item.source,type:item.type,lang:item.lang,url:`/${item.lang}/${item.type}/${item.slug}/`,tags:item.tags||[]});}
fs.writeFileSync(path.join(out,'search-index.json'),JSON.stringify(search));
fs.writeFileSync(path.join(out,'index.html'),`<!doctype html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Eularcat</title><meta name="description" content="${escape(copy.zh.intro)}"><link rel="icon" href="/favicon.svg"><script src="/assets/locale.js"></script></head><body><a href="/zh/">中文</a> · <a href="/en/">English</a></body></html>`);
fs.writeFileSync(path.join(out,'404.html'),layout({lang:'zh',route:'404',title:copy.zh.notFound,description:copy.zh.notFoundText,origin,alternate:false,body:pageHeader('404',copy.zh.notFound,copy.zh.notFoundText)+`<div class="wrap page-body"><a class="button primary" href="/zh/">${copy.zh.home}</a></div>`}));
const xml=value=>escape(value);
fs.writeFileSync(path.join(out,'sitemap.xml'),`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">${urls.map(u=>`<url><loc>${xml(origin+u.path)}</loc>${u.alternate?['zh','en'].map(l=>`<xhtml:link rel="alternate" hreflang="${l}" href="${xml(origin+u.path.replace(/^\/(zh|en)\//,'/'+l+'/'))}"/>`).join(''):''}</url>`).join('')}</urlset>`);
fs.writeFileSync(path.join(out,'robots.txt'),`User-agent: *\nAllow: /\nSitemap: ${origin}/sitemap.xml\n`);
fs.writeFileSync(path.join(out,'feed.xml'),`<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Eularcat</title><link>${xml(origin)}</link><description>${xml(copy.zh.intro)}</description>${items.map(x=>`<item><title>${xml(x.title)}</title><link>${xml(origin+'/'+x.lang+'/'+x.type+'/'+x.slug+'/')}</link><guid>${xml(origin+'/'+x.lang+'/'+x.type+'/'+x.slug+'/')}</guid><description>${xml(x.description||'')}</description>${x.date?`<pubDate>${new Date(x.date+'T00:00:00Z').toUTCString()}</pubDate>`:''}</item>`).join('')}</channel></rss>`);
console.log(`Built ${urls.length} pages, ${items.length} published content entries. Origin: ${origin}`);

