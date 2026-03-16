
/**
 * AGENDA SEMANAL – PREMIUM: colapsar/expandir por dia
 * Requisitos (já existem no seu HTML/CSS):
 * - colunas: .day-col
 * - corpo do dia: .day-body
 * - cards: .agenda-card
 */
(function(){
  const MAX_VISIBLE = 3; // <- ajuste aqui se quiser (ex.: 4)

  function setupDay(dayCol){
    const body = dayCol.querySelector('.day-body');
    if(!body) return;

    const cards = Array.from(body.querySelectorAll('.agenda-card'));
    if(cards.length <= MAX_VISIBLE) return;

    // esconde excedentes
    cards.forEach((c, idx) => {
      if(idx >= MAX_VISIBLE) c.classList.add('appt-hidden');
    });

    const hiddenCount = cards.length - MAX_VISIBLE;

    // cria botão
    const wrap = document.createElement('div');
    wrap.className = 'day-more';

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = `+ ${hiddenCount} agendamentos (ver mais)`;

    let expanded = false;

    btn.addEventListener('click', () => {
      expanded = !expanded;
      dayCol.classList.toggle('is-expanded', expanded);

      cards.forEach((c, idx) => {
        if(idx >= MAX_VISIBLE){
          c.classList.toggle('appt-hidden', !expanded);
        }
      });

      btn.textContent = expanded ? 'Mostrar menos' : `+ ${hiddenCount} agendamentos (ver mais)`;

      if(!expanded){
        body.scrollTop = 0;
        dayCol.scrollIntoView({behavior:'smooth', block:'nearest', inline:'nearest'});
      }
    });

    wrap.appendChild(btn);
    dayCol.appendChild(wrap);
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.day-col').forEach(setupDay);
  });
})();
