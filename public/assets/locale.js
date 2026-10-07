try{const saved=localStorage.getItem('eularcat-language');const lang=saved||((navigator.language||'zh').startsWith('zh')?'zh':'en');location.replace('/'+lang+'/');}catch{location.replace('/zh/');}
