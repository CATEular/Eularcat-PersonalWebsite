import test from 'node:test';
import assert from 'node:assert/strict';
import {library,ai,about,learn} from '../src/components/pages.mjs';
import fs from 'node:fs';
test('reading filters reflect unique published record tags, including arbitrary user tags',()=>{
 const html=library('zh','reading',[{type:'reading',lang:'zh',slug:'one',title:'One',tags:['用户自定义','Buck']},{type:'reading',lang:'zh',slug:'two',title:'Two',tags:['用户自定义']}]);
 assert.equal((html.match(/data-filter="用户自定义"/g)||[]).length,1);
 assert.match(html,/data-filter="Buck"/);
 assert.doesNotMatch(html,/data-filter="(?:COT|Comparator|LDO|PMIC)"/);
 assert.equal((library('zh','reading',[]).match(/data-filter=/g)||[]).length,1);
});
test('AI workflows show categories without inventing cases, and only link published notes',()=>{
 const data=JSON.parse(fs.readFileSync('content/ai-ic.json','utf8'));
 const html=ai('zh',data,[]);
 assert.equal((html.match(/class="workflow-empty"/g)||[]).length,4);
 assert.doesNotMatch(html,/workflow-steps|workflow-records/);
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
