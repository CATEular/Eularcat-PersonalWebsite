// Navigation follows the user's input modality; keyboard and reduced motion are immediate.
(()=>{
 const reduced=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
 let keyboard=false;
 document.addEventListener('pointerdown',()=>keyboard=false,{capture:true,passive:true});
 document.addEventListener('keydown',()=>keyboard=true,{capture:true});
 window.addEventListener('pageswap',event=>{
  const skip=keyboard||reduced();
  try{sessionStorage.setItem('eularcat-skip-transition',String(skip));}catch{}
  if(skip)event.viewTransition?.skipTransition();
 });
 window.addEventListener('pagereveal',event=>{
  let skip=reduced();try{skip ||= sessionStorage.getItem('eularcat-skip-transition')==='true';sessionStorage.removeItem('eularcat-skip-transition');}catch{}
  if(skip)event.viewTransition?.skipTransition();
 });
 // Browsers without cross-document transitions still get a short, non-blocking entrance.
 if(!('onpagereveal' in window))document.addEventListener('DOMContentLoaded',()=>{
  if(reduced()||keyboard)return;
  document.querySelector('main')?.animate([{opacity:0,transform:'translateY(8px)'},{opacity:1,transform:'none'}],{duration:240,easing:'cubic-bezier(.23,1,.32,1)'});
 });
})();
