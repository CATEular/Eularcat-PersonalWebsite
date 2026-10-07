import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import matter from 'gray-matter';
import {normalizePaper,importObsidianPaper} from './obsidian-paper.mjs';
const source=`---
title: Real paper
authors: Alice, Bob
publication: JSSC
published: '2004'
source_url: https://doi.org/example
created: '2026-09-11'
status: analyzed
tags: [Buck]
---
# Real paper
## References
[[[JSSC-2024] Other paper|Original citation label]]
![[diagram.png|400]]
\`\`\`text
[[literal syntax]]
\`\`\`
`;
test('Obsidian paper metadata is normalized, unpublished references remain readable and code remains literal',()=>{
 const result=matter(normalizePaper(source));
 assert.deepEqual(result.data.authors,['Alice','Bob']);assert.equal(result.data.year,2004);assert.equal(result.data.venue,'JSSC');assert.equal(result.data.status,'draft');assert.equal(result.data.url,'https://doi.org/example');assert.equal(result.data.date,'2026-09-11');
 assert.doesNotMatch(result.content,/# Real paper|\[\[\[JSSC/);assert.match(result.content,/Original citation label/);assert.match(result.content,/!\[\[diagram.png\|400\]\]/);assert.match(result.content,/\[\[literal syntax\]\]/);
 assert.equal(matter(normalizePaper(source,{publish:true})).data.status,'published');
});
test('paper import leaves the source untouched and carries its actual image into the site',()=>{
 const temp=fs.mkdtempSync(path.join(os.tmpdir(),'eularcat-import-test-'));
 try{
  const note=path.join(temp,'source.md');fs.writeFileSync(note,source);fs.writeFileSync(path.join(temp,'diagram.png'),'test image bytes');
  const result=importObsidianPaper({note,root:temp,slug:'real-paper'});
  assert.equal(fs.readFileSync(note,'utf8'),source);assert.equal(result.assets,1);assert.equal(result.status,'draft');
  assert.match(fs.readFileSync(path.join(result.directory,'note.md'),'utf8'),/\.\/assets\/diagram.png/);
  assert.throws(()=>importObsidianPaper({note,root:temp,slug:'real-paper'}),/will not overwrite/);
 }finally{fs.rmSync(temp,{recursive:true,force:true});}
});
