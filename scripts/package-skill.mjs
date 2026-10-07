import fs from 'node:fs';
import path from 'node:path';
import {zipSync} from 'fflate';
export const skillFiles=['SKILL.md','config.example.json','requirements.txt','scripts/paths.py','scripts/extract_figures.py','resources/analog_paper_template.md','resources/buck_paper_template.md','references/pmic_fom_and_terms.md','references/figures.md'];
export function packageSkill(root,out){
 const source=path.join(root,'skills','analog-ic-notes'),files={};
 for(const name of skillFiles){const bytes=fs.readFileSync(path.join(source,name));const text=bytes.toString('utf8');if(/(?:[A-Za-z]:[\\/]|\/Users\/|\/home\/[^/\s]+\/)/i.test(text))throw new Error('Personal path or private identifier in skill export: '+name);files['analog-ic-notes/'+name]=new Uint8Array(bytes);const target=path.join(out,'downloads','analog-ic-notes',name);fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,bytes);}
 fs.writeFileSync(path.join(out,'downloads','analog-ic-notes.zip'),zipSync(files,{level:6}));
}
