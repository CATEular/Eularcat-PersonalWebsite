import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {unzipSync} from 'fflate';
import {packageVirtuoso} from './package-virtuoso.mjs';

test('Virtuoso downloads are complete, reproducible and exclude private configuration and presets',()=>{
 const temporary=fs.mkdtempSync(path.join(os.tmpdir(),'virtuoso-export-'));
 try{
  const source=path.join(temporary,'skills','virtuoso-workflow');
  fs.cpSync('skills/virtuoso-workflow',source,{recursive:true});
  fs.writeFileSync(path.join(source,'virtuoso-connect','config.local.json'),'{"private":"never export"}');
  fs.mkdirSync(path.join(source,'virtuoso-connect','agents'));fs.writeFileSync(path.join(source,'virtuoso-connect','agents','openai.yaml'),'private preset');
  const out=path.join(temporary,'out');packageVirtuoso(temporary,out);
  const archive=fs.readFileSync(path.join(out,'downloads','virtuoso-workflow.zip')),files=unzipSync(archive),manifest=JSON.parse(fs.readFileSync(path.join(source,'export-manifest.json'),'utf8'));
  assert.deepEqual(Object.keys(files).sort(),[...manifest,'export-manifest.json'].map(x=>'virtuoso-workflow/'+x).sort());
  for(const name of [...manifest,'export-manifest.json'])assert.deepEqual(Buffer.from(files['virtuoso-workflow/'+name]),Buffer.from(fs.readFileSync(path.join(source,name),'utf8').replace(/\r\n/g,'\n')));
  for(const name of ['connect','testbench','params','layout','helper'])assert.ok(files[`virtuoso-workflow/virtuoso-${name}/SKILL.md`]);
  assert.ok(!Object.keys(files).some(x=>/config\.local|agents\/|\.env|\.log/.test(x)));
  packageVirtuoso(temporary,out);assert.deepEqual(fs.readFileSync(path.join(out,'downloads','virtuoso-workflow.zip')),archive);
  assert.deepEqual(fs.readFileSync('public/downloads/virtuoso-workflow.zip'),archive,'Refresh the reviewed GitHub ZIP after changing product files');
  fs.appendFileSync(path.join(source,'virtuoso-connect','SKILL.md'),'\nZ:/Private/project');
  assert.throws(()=>packageVirtuoso(temporary,out),/Private information/);
 }finally{fs.rmSync(temporary,{recursive:true,force:true});}
});

test('export rejects traversal and missing sibling references',()=>{
 const temporary=fs.mkdtempSync(path.join(os.tmpdir(),'virtuoso-manifest-'));
 try{
  const source=path.join(temporary,'skills','virtuoso-workflow');fs.cpSync('skills/virtuoso-workflow',source,{recursive:true});
  fs.appendFileSync(path.join(source,'virtuoso-connect','SKILL.md'),'\n[Missing](../missing/SKILL.md)');
  assert.throws(()=>packageVirtuoso(temporary,path.join(temporary,'out')),/Unpackaged reference/);
  fs.writeFileSync(path.join(source,'export-manifest.json'),'["../secret.txt"]');
  assert.throws(()=>packageVirtuoso(temporary,path.join(temporary,'out')),/Forbidden Virtuoso export path/);
 }finally{fs.rmSync(temporary,{recursive:true,force:true});}
});
