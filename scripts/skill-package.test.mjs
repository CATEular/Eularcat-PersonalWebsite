import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {unzipSync,strFromU8} from 'fflate';
import {packageSkill,skillFiles} from './package-skill.mjs';

test('skill export includes complete usable sources and excludes local configuration',()=>{
 const temporary=fs.mkdtempSync(path.join(os.tmpdir(),'analog-ic-export-'));
 try{
  const source=path.join(temporary,'skills','analog-ic-notes');
  fs.cpSync('skills/analog-ic-notes',source,{recursive:true});
  fs.writeFileSync(path.join(source,'config.local.json'),JSON.stringify({paths:{notes:'E:/Private/Notes'}}));
  const output=path.join(temporary,'dist');packageSkill(temporary,output);
  const files=unzipSync(fs.readFileSync(path.join(output,'downloads','analog-ic-notes.zip')));
  assert.deepEqual(Object.keys(files).sort(),skillFiles.map(x=>'analog-ic-notes/'+x).sort());
  for(const name of skillFiles)assert.deepEqual(Buffer.from(files['analog-ic-notes/'+name]),fs.readFileSync(path.join(source,name)));
  const config=JSON.parse(strFromU8(files['analog-ic-notes/config.example.json']));
  assert.equal(config.paths.notes,'./notes');
  assert.equal(fs.existsSync(path.join(output,'downloads','analog-ic-notes','config.local.json')),false);
  fs.appendFileSync(path.join(source,'SKILL.md'),'\nE:\\Private\\Notes');
  assert.throws(()=>packageSkill(temporary,output),/Personal path/);
 }finally{fs.rmSync(temporary,{recursive:true,force:true});}
});
