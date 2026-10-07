try { const choice=localStorage.getItem('eularcat-theme'); document.documentElement.dataset.theme=choice|| (matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'); } catch {}
