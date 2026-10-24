import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {unzipSync} from 'fflate';
import {packageZotero,zoteroFiles} from './package-zotero.mjs';

test('Zotero download excludes local preferences, evidence and agent presets',()=>{
 const temporary=fs.mkdtempSync(path.join(os.tmpdir(),'zotero-export-'));
 try{
  const source=path.join(temporary,'skills','zotero-reading-notes');
  fs.cpSync('skills/zotero-reading-notes',source,{recursive:true});
  fs.writeFileSync(path.join(source,'config.local.json'),'{"vault":"private"}');
  fs.writeFileSync(path.join(source,'evidence.json'),'{"paperKey":"PRIVATE1"}');
  fs.mkdirSync(path.join(source,'agents'));fs.writeFileSync(path.join(source,'agents/openai.yaml'),'private preset');
  const output=path.join(temporary,'dist');packageZotero(temporary,output);
  const files=unzipSync(fs.readFileSync(path.join(output,'downloads/zotero-reading-notes.zip')));
  assert.deepEqual(Object.keys(files).sort(),zoteroFiles.map(x=>'zotero-reading-notes/'+x).sort());
  for(const name of zoteroFiles)assert.deepEqual(Buffer.from(files['zotero-reading-notes/'+name]),fs.readFileSync(path.join(source,name)));
  fs.appendFileSync(path.join(source,'SKILL.md'),'\nE:\\Private\\Notes');
  assert.throws(()=>packageZotero(temporary,output),/Personal path/);
 }finally{fs.rmSync(temporary,{recursive:true,force:true});}
});
