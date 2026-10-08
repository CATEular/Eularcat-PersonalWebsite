const lang=document.documentElement.lang;
const container=document.querySelector('[data-conversation]');
if(container){
 const turns=[...container.querySelectorAll('[data-stage]')],buttons=[...container.querySelectorAll('[data-turn]')];
 const previous=container.querySelector('[data-previous-turn]'),next=container.querySelector('[data-next-turn]'),progress=container.querySelector('[data-turn-progress]'),toggle=document.querySelector('[data-show-transcript]');
 let selected=0,all=false;
 container.querySelector('.conversation-turns').hidden=false;container.querySelector('.conversation-controls').hidden=false;toggle.hidden=false;
 const hashIndex=turns.findIndex(x=>'#'+x.id===location.hash);if(hashIndex>=0)selected=hashIndex;
 function render(){turns.forEach((turn,i)=>{turn.hidden=!all&&i!==selected;buttons[i].setAttribute('aria-expanded',String(all||i===selected));if(i===selected)buttons[i].setAttribute('aria-current','step');else buttons[i].removeAttribute('aria-current');});previous.disabled=selected===0;next.disabled=selected===turns.length-1;progress.textContent=`${selected+1} / ${turns.length}`;toggle.setAttribute('aria-pressed',String(all));toggle.textContent=lang==='zh'?(all?'逐轮阅读':'展开整段对话'):(all?'Read turn by turn':'Show the full conversation');}
 function go(i,focus=true){selected=Math.max(0,Math.min(turns.length-1,i));all=false;render();history.replaceState(null,'','#'+turns[selected].id);if(focus){turns[selected].tabIndex=-1;turns[selected].focus({preventScroll:true});turns[selected].scrollIntoView({behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth',block:'start'});}}
 buttons.forEach((button,i)=>button.addEventListener('click',()=>go(i)));previous.addEventListener('click',()=>go(selected-1));next.addEventListener('click',()=>go(selected+1));toggle.addEventListener('click',()=>{all=!all;render();});
 addEventListener('hashchange',()=>{const i=turns.findIndex(x=>'#'+x.id===location.hash);if(i>=0)go(i,false);});render();
}
document.querySelectorAll('.virtuoso-guide pre code').forEach(code=>{
 if(!code.textContent.includes('skills/virtuoso-workflow/README.md'))return;
 const pre=code.parentElement,wrapper=document.createElement('div'),button=document.createElement('button');
 wrapper.dataset.installPrompt='';wrapper.className='install-prompt';code.dataset.promptText='';button.type='button';button.className='button secondary';button.textContent=lang==='zh'?'复制安装指令':'Copy installation prompt';pre.before(wrapper);wrapper.append(button,pre);
});
document.querySelectorAll('[data-copy-prompt], [data-install-prompt] button').forEach(button=>{button.hidden=false;button.addEventListener('click',async()=>{const parent=button.closest('.dialogue-message,[data-install-prompt]');const text=parent.querySelector('[data-prompt-text]').textContent;const status=document.querySelector('[data-copy-status]');try{await navigator.clipboard.writeText(text);button.textContent=lang==='zh'?'已复制':'Copied';if(status)status.textContent=lang==='zh'?'已复制，可粘贴到 Agent 对话中。':'Copied. Paste it into your agent conversation.';}catch{button.textContent=lang==='zh'?'请手动复制下方文字':'Select and copy the text';if(status)status.textContent=lang==='zh'?'复制未完成，请选中提问文字手动复制。':'Select the prompt text and copy it manually.';}});});
