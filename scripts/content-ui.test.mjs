import test from 'node:test';
import assert from 'node:assert/strict';
import {library,ai,about,learn} from '../src/components/pages.mjs';
import {learningTiles} from '../src/components/home.mjs';
import fs from 'node:fs';
import {renderMarkdown} from '../src/markdown.mjs';

test('Buck ESR and DCR key equations have sequential, renderable numbers',()=>{
 for(const slug of ['buck-esr-ripple','buck-dcr']){
  const source=fs.readFileSync(`content/notes/${slug}/index.md`,'utf8');
  const numbers=[...source.matchAll(/\\tag\{(\d+)\}/g)].map(match=>Number(match[1]));
  assert.deepEqual(numbers,Array.from({length:18},(_,index)=>index+1),slug);
  const html=renderMarkdown(source).html;
  assert.doesNotMatch(html,/katex-error/,slug);
  assert.equal((html.match(/class="tag"/g)||[]).length,18,slug);
 }
});
test('published Virtuoso prose renders emphasis instead of literal Markdown markers',()=>{
 const root='content/workflows/virtuoso';
 for(const file of fs.readdirSync(root).filter(name=>name.endsWith('.md'))){
  const html=renderMarkdown(fs.readFileSync(`${root}/${file}`,'utf8')).html.replace(/<pre[\s\S]*?<\/pre>/g,'');
  assert.doesNotMatch(html,/\*\*/,file);
 }
 const osc=renderMarkdown(fs.readFileSync(`${root}/osc.zh.md`,'utf8')).html;
 assert.match(osc,/<strong>技能接力：<\/strong> connect/);
});
test('reading filters reflect unique published record tags, including arbitrary user tags',()=>{
 const html=library('zh','reading',[{type:'reading',lang:'zh',slug:'one',title:'One',tags:['用户自定义','Buck']},{type:'reading',lang:'zh',slug:'two',title:'Two',tags:['用户自定义']}]);
 assert.equal((html.match(/data-filter="用户自定义"/g)||[]).length,1);
 assert.match(html,/data-filter="Buck"/);
 assert.doesNotMatch(html,/data-filter="(?:COT|Comparator|LDO|PMIC)"/);
 assert.equal((library('zh','reading',[]).match(/data-filter=/g)||[]).length,1);
});
test('AI workflows link reviewed case records and only link published notes',()=>{
 const data=JSON.parse(fs.readFileSync('content/ai-ic.json','utf8'));
 const html=ai('zh',data,[]);
 assert.equal((html.match(/class="workflow-empty"/g)||[]).length,0);
 assert.match(html,/ai-ic\/virtuoso-workflow\/osc/);
 assert.match(html,/ai-ic\/virtuoso-workflow\/mos/);
 assert.match(html,/版图技能使用说明/);
 assert.match(html,/downloads\/analog-ic-notes.zip/);
 data.workflows[0].notes=['real','draft','missing'];
 const populated=ai('zh',data,[{type:'notes',slug:'real',lang:'zh',title:'真实记录',status:'published'},{type:'notes',slug:'draft',lang:'zh',title:'草稿记录',status:'draft'}]);
 assert.match(populated,/href="\/zh\/notes\/real\/"/);
 assert.doesNotMatch(populated,/草稿记录|notes\/missing/);
});
test('About has no editing controls in either locale',()=>{
 for(const lang of ['zh','en'])assert.doesNotMatch(about(lang,{title:'Eularcat',html:'<p>About</p>',toc:[]}),/about\/edit|editor|编辑 About|Edit About/);
});
test('note filters use stable categories independent of locale or rendering-test label',()=>{
 for(const lang of ['zh','en']){
  const html=library(lang,'notes',[{type:'notes',category:'knowledge',test:true,lang:'zh',slug:'one',title:'One'},{type:'notes',category:'engineering',lang:'zh',slug:'two',title:'Two'}]);
  assert.match(html,/data-category="knowledge"/);assert.match(html,/data-category="engineering"/);
 }
});
test('learning map follows the configured hierarchy and renders every group anchor',()=>{
 const site=JSON.parse(fs.readFileSync('content/site.json','utf8'));
 assert.deepEqual(site.learning.map(x=>x.category),['power','buck','multiphase','ai-eda']);
 const html=learn('zh',site,[]);
 for(const group of site.learning){assert.ok(html.includes('id="'+group.category+'"'));assert.ok(html.includes(group.title.zh));}
 assert.ok(html.indexOf('功率及电路基础')<html.indexOf('同步 DC-DC Buck'));
});
test('atlas links existing notes and legacy learning articles while notes remain independent',()=>{
 const site={learning:[{category:'power',code:'POWER',glyph:'P',eyebrow:'POWER',title:{zh:'基础',en:'Basics'},description:{zh:'目录',en:'Index'},topics:['Buck']} ]};
 const records=[
  {type:'notes',slug:'day-one',lang:'zh',title:'第一天',topic:'Buck',status:'published'},
  {type:'learn',slug:'legacy',lang:'en',title:'Legacy',topic:'Buck',status:'published'},
  {type:'notes',slug:'draft',lang:'zh',title:'未公开',topic:'Buck',status:'draft'},
  {type:'notes',slug:'other',lang:'zh',title:'目录之外',status:'published'}
 ];
 for(const lang of ['zh','en']){
  const html=learn(lang,site,records);
  assert.match(html,/href="\/zh\/notes\/day-one\/"/);
  assert.match(html,/href="\/en\/learn\/legacy\/"/);
  assert.doesNotMatch(html,/未公开|notes\/other|learn\/day-one/);
  assert.match(learningTiles(lang,site,records),lang==='zh'?/2 篇笔记/:/2 notes/);
 }
 assert.match(library('zh','notes',records.filter(x=>x.status==='published')),/notes\/other/);
});
