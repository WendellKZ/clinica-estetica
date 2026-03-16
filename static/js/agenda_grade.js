(function(){
  const START = 8*60;   // 08:00
  const END   = 21*60;  // 21:00
  const PX_PER_MIN = 1; // 60px por hora

  function parseHM(hm){
    const [h,m] = hm.split(':').map(x=>parseInt(x,10));
    return h*60 + m;
  }

  function buildTimeCol(){
    const col = document.getElementById('timeCol');
    if(!col) return;
    col.innerHTML = '';
    for(let t=START; t<=END; t+=60){
      const h = String(Math.floor(t/60)).padStart(2,'0') + ':00';
      const div = document.createElement('div');
      div.className = 'time-slot';
      div.textContent = h;
      col.appendChild(div);
    }
  }

  function layout(){
    const events = document.querySelectorAll('.event[data-start][data-end]');
    events.forEach(ev=>{
      const s = parseHM(ev.dataset.start);
      const e = parseHM(ev.dataset.end);
      const top = Math.max(0, (s-START)*PX_PER_MIN);
      const h = Math.max(34, (e-s)*PX_PER_MIN);
      ev.style.top = top + 'px';
      ev.style.height = h + 'px';
    });
  }

  // navegação data
  window.navDay = function(delta){
    const input = document.querySelector('input[type="date"][name="data"]');
    if(!input || !input.value) return;
    const d = new Date(input.value + 'T00:00:00');
    d.setDate(d.getDate() + delta);
    const y = d.getFullYear();
    const m = String(d.getMonth()+1).padStart(2,'0');
    const day = String(d.getDate()).padStart(2,'0');
    input.value = `${y}-${m}-${day}`;
    input.form.submit();
  }
  window.goToday = function(){
    const input = document.querySelector('input[type="date"][name="data"]');
    if(!input) return;
    const d = new Date();
    const y = d.getFullYear();
    const m = String(d.getMonth()+1).padStart(2,'0');
    const day = String(d.getDate()).padStart(2,'0');
    input.value = `${y}-${m}-${day}`;
    input.form.submit();
  }

  buildTimeCol();
  layout();
})();