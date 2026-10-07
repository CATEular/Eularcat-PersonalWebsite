import MarkdownIt from 'markdown-it';
import texmath from 'markdown-it-texmath';
import katex from 'katex';
import hljs from 'highlight.js';
const escape = value => String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const md=new MarkdownIt({html:false,linkify:true,typographer:false,highlight:(text,lang)=>lang&&hljs.getLanguage(lang)?hljs.highlight(text,{language:lang,ignoreIllegals:true}).value:escape(text)}).use(texmath,{engine:katex,delimiters:'dollars',katexOptions:{throwOnError:false,trust:false,strict:'warn'}});
const defaultTableOpen=md.renderer.rules.table_open;md.renderer.rules.table_open=(...args)=>'<div class="table-scroll">'+(defaultTableOpen?defaultTableOpen(...args):'<table>');md.renderer.rules.table_close=()=>'</table></div>';
const defaultImage=md.renderer.rules.image;md.renderer.rules.image=(tokens,idx,options,env,self)=>{const title=tokens[idx].attrGet('title');const img=defaultImage(tokens,idx,options,env,self);return title?`<span class="figure">${img}<span class="image-caption" style="display:block">${escape(title)}</span></span>`:img;};
const slugify=text=>String(text).normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{N}]+/gu,'-').replace(/^-|-$/g,'')||'section';
export function renderMarkdown(text){const tokens=md.parse(text,{}),toc=[],used=new Map();for(let i=0;i<tokens.length;i++){if(tokens[i].type==='heading_open'){const title=tokens[i+1].content,base=slugify(title),count=used.get(base)||0,id=base+(count?'-'+count:'');used.set(base,count+1);tokens[i].attrSet('id',id);if(['h2','h3'].includes(tokens[i].tag))toc.push({title,id,level:tokens[i].tag});}}return {html:md.renderer.render(tokens,md.options,{}),toc};}
