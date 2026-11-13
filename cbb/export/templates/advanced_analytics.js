/* Advanced analysis uses the current competition and team; no sample data is mixed in. */
const markovDemo = JSON.parse($('markov-demo-data').textContent);
const compareControl = $('compare-team');
const fmt2=value=>new Intl.NumberFormat('pt-BR',{minimumFractionDigits:2,maximumFractionDigits:2}).format(value);
let comparisonCompetition = '';
function totalsForAnalysis(c,t,selectedGames=null) {
  const games=selectedGames||teamGames(c,t), sample=playerData(c,t,games);
  const sum=key=>sample.players.reduce((a,p)=>a+(Number(p[key])||0),0);
  let two=sum('two'),three=sum('three'),twoMade=sum('twoMade'),threeMade=sum('threeMade'),teamOnlyGames=0;
  // A full-game LNB box score can supply team shooting when the event map is absent.
  if(c.type==='nbb'&&Number($('quarter').value)===0){
    const kind=Number($('shot-type').value);
    for(const game of games){
      if(game.shots?.length)continue;
      const side=names(game,c).indexOf(t), box=game.boxscore?.[side];
      if(!Array.isArray(box)||box.length!==4||!box.every(x=>x!==null&&x!==undefined&&Number.isFinite(Number(x))&&Number(x)>=0)||Number(box[0])>Number(box[1])||Number(box[2])>Number(box[3])||Number(box[1])+Number(box[3])===0)continue;
      if(!kind||kind===2){twoMade+=Number(box[0]);two+=Number(box[1])}
      if(!kind||kind===3){threeMade+=Number(box[2]);three+=Number(box[3])}
      teamOnlyGames++;
    }
  }
  const attempts=two+three, ft=c.type==='cbi'?sum('ft'):null, validPoints=c.type==='cbi'?sum('validPoints'):null;
  return {games,sample,two,three,twoMade,threeMade,attempts,ft,teamCovered:(c.type==='cbi'?0:sample.covered+teamOnlyGames),teamOnlyGames,
    efg:attempts?(twoMade+1.5*threeMade)/attempts:null,
    threeRate:attempts?three/attempts:null,
    ftr:attempts&&ft!==null?ft/attempts:null, ts:ft!==null&&attempts+0.44*ft>0?validPoints/(2*(attempts+0.44*ft)):null};
}

function statCard(label,value,detail){return '<div class="card"><span>'+esc(label)+'</span><strong>'+esc(value)+'</strong><small>'+esc(detail)+'</small></div>'}
function formatPercent(value){return value===null?'—':fmt(value*100)+'%'}
function quarterShots(c,t,ignoreQuarter=false){
  if(c.type!=='nbb')return [];
  const q=Number($('quarter').value), kind=Number($('shot-type').value), items=[];
  for(const game of teamGames(c,t)){
    const side=names(game,c).indexOf(t);
    for(const sh of game.shots||[]){
      if(sh[0]!==side||(kind&&sh[3]!==kind))continue;
      if(!ignoreQuarter&&q&&(q===5?sh[2]<5:sh[2]!==q))continue;
      items.push({shot:sh,game});
    }
  }
  return items;
}
function renderAdvanced(){
  const c=selectedCompetition(),t=team.value;if(!c||!t)return;
  const data=totalsForAnalysis(c,t), s=data.sample;
  $('advanced-cards').innerHTML=[
    statCard('eFG%',formatPercent(data.efg),'cestas de 3 têm peso adicional'),
    statCard('Frequência de 3',formatPercent(data.threeRate),'tentativas de 3 / tentativas de quadra'),
    statCard('FTR',data.ftr===null?'—':fmt2(data.ftr),'lances livres tentados / arremessos de quadra'),
    statCard('TS%',formatPercent(data.ts),'pontuação por tentativas estimadas')
  ].join('');
  $('advanced-coverage').textContent=c.type==='cbi'?`Amostra: ${s.covered} de ${data.games.length} jogos com súmula individual conferida. Pontos e cestas convertidas podem ser analisados; tentativas erradas não estão confirmadas, portanto os indicadores de aproveitamento ficam indisponíveis.`:`Amostra: ${data.attempts} tentativas de quadra em ${data.teamCovered} de ${data.games.length} jogos com registros de equipe. ${s.covered} jogos têm arremessos individuais identificados; ${data.teamOnlyGames} adicionais fornecem apenas totais de equipe. Esses totais só entram quando o período selecionado é “Todos”. O FTR não está disponível nesta base.`;
  renderAdvancedDistribution(c,t,data);
  renderAdvancedMap(c,t);
  renderAdvancedPeriods(c,t);
  renderShotMix(data);
  renderGameEfg(c,t,data.games);
  renderAdvancedTrend(c,t,data.games);
  renderTactical(c,t,data);
  if(comparisonCompetition!==c.id){
    const teams=[...new Set(c.games.flatMap(g=>names(g,c)))].filter(Boolean).sort((a,b)=>a.localeCompare(b,'pt-BR'));
    compareControl.replaceChildren(...teams.map(name=>new Option(name,name)));comparisonCompetition=c.id;
    compareControl.value=teams.find(name=>name!==t)||t;
  }else if(compareControl.value===t){
    const alternatives=[...compareControl.options].map(o=>o.value);compareControl.value=alternatives.find(x=>x!==t)||t;
  }
  renderAdvancedComparison();
}
function renderAdvancedDistribution(c,t,data){
  let players=data.sample.players.map(p=>({id:p.id,name:p.name,attempts:(p.two||0)+(p.three||0),prior:0}));
  const q=Number($('quarter').value);let priorTotal=0, sampleGames=0;
  if(c.type==='nbb'&&q){
    const kind=Number($('shot-type').value), known=new Map(players.map(p=>[p.id,p]));
    for(const g of data.games){let has=false;const side=names(g,c).indexOf(t);
      for(const sh of g.shots||[]){if(sh[0]!==side||(kind&&sh[3]!==kind))continue;const inPeriod=q===5?sh[2]>=5:sh[2]===q,id=String(sh[1]);if(inPeriod){has=true;continue}
        let p=known.get(id);if(!p){p={id,name:g.players[id]||'Atleta',attempts:0,prior:0};known.set(id,p)}p.prior++;priorTotal++;
      }if(has)sampleGames++;
    }players=[...known.values()];
  }
  const total=players.reduce((n,p)=>n+p.attempts,0),adjusted=c.type==='nbb'&&q>0&&total>=20&&sampleGames>=3&&priorTotal>0;
  players=players.filter(p=>p.attempts>0||(adjusted&&p.prior>0)).map(p=>({...p,share:total?p.attempts/total:0,adjusted:adjusted?(p.attempts+20*p.prior/priorTotal)/(total+20):null})).sort((a,b)=>(b.adjusted??b.share)-(a.adjusted??a.share));
  bars('advanced-distribution',players.slice(0,10).map(p=>({name:p.name,value:p.share*100,text:formatPercent(p.share)})));
  $('advanced-shrinkage').textContent=adjusted?`Fatia ajustada: combina ${total} tentativas em ${sampleGames} jogos com 20 tentativas equivalentes distribuídas conforme os ${priorTotal} arremessos dos outros períodos. É uma descrição histórica, não previsão de acionamento.`:(c.type==='nbb'&&q?'Fatia ajustada indisponível: exige pelo menos 20 tentativas em três jogos no período selecionado e referência em outros períodos.':'Selecione um período no NBB ou na LDB para avaliar a fatia ajustada; o ajuste requer amostra mínima. O CBI ainda não fornece esse recorte na base.');
  $('advanced-distribution-table').innerHTML=players.length?players.map(p=>'<tr><td>'+esc(p.name)+'</td><td class="num">'+p.attempts+'</td><td class="num">'+formatPercent(p.share)+'</td><td class="num">'+formatPercent(p.adjusted)+'</td></tr>').join(''):'<tr><td colspan="4">Nenhuma tentativa identificada neste recorte.</td></tr>';
}
function renderAdvancedMap(c,t){
  const root=$('advanced-map');$('map-controls').hidden=c.type!=='nbb';if(c.type!=='nbb'){root.innerHTML='<div class="empty">A fonte CBI desta base ainda não fornece coordenadas dos arremessos. Consulte as súmulas individuais na aba Jogos.</div>';return}
  const resultFilter=$('map-result').value;
  const shots=quarterShots(c,t).map(x=>x.shot).filter(sh=>(resultFilter!=='made'||!!sh[4])&&(resultFilter!=='missed'||!sh[4])).filter(sh=>sh[5]!==null&&sh[5]!==undefined&&sh[6]!==null&&sh[6]!==undefined&&Number.isFinite(Number(sh[5]))&&Number.isFinite(Number(sh[6]))&&sh[5]>=0&&sh[5]<=100&&sh[6]>=0&&sh[6]<=100);
  if(!shots.length){root.innerHTML='<div class="empty">Sem coordenadas disponíveis neste recorte ou filtro de resultado.</div>';return}
  // The original LNB graphic is horizontal (623 × 345); left/top are percentages of that image.
  const markers=shots.map(sh=>{const x=Number(sh[5])*6.23,y=Number(sh[6])*3.45;return sh[4]?`<circle cx="${x.toFixed(2)}" cy="${y.toFixed(2)}" r="4" fill="#75ced5" stroke="#12323c" stroke-width="1.2" opacity=".9"><title>Convertido · ${sh[3]} pontos</title></circle>`:`<path d="M ${(x-3.8).toFixed(2)} ${(y-3.8).toFixed(2)} L ${(x+3.8).toFixed(2)} ${(y+3.8).toFixed(2)} M ${(x+3.8).toFixed(2)} ${(y-3.8).toFixed(2)} L ${(x-3.8).toFixed(2)} ${(y+3.8).toFixed(2)}" stroke="#8d291c" stroke-width="2.5" stroke-linecap="round"><title>Não convertido · ${sh[3]} pontos</title></path>`}).join('');
  const court=`<rect width="623" height="345" fill="#c99060"/><path d="M 0 55 H 623 M 0 110 H 623 M 0 165 H 623 M 0 220 H 623 M 0 275 H 623" stroke="#9d704e" stroke-width="1" opacity=".25"/><rect x="12" y="10" width="599" height="323" fill="none" stroke="#fff3df" stroke-width="3"/><rect x="12" y="123" width="120" height="98" fill="#8e6044" fill-opacity=".5" stroke="#fff3df" stroke-width="3"/><rect x="491" y="123" width="120" height="98" fill="#8e6044" fill-opacity=".5" stroke="#fff3df" stroke-width="3"/><g fill="none" stroke="#fff3df" stroke-width="3"><path d="M 312 10 V 333"/><circle cx="312" cy="172" r="40"/><path d="M 12 32 H 90 C 148 32 197 99 197 172 C 197 245 148 312 90 312 H 12"/><path d="M 611 32 H 533 C 475 32 426 99 426 172 C 426 245 475 312 533 312 H 611"/><path d="M 132 132 A 40 40 0 0 1 132 212"/><path d="M 491 132 A 40 40 0 0 0 491 212"/><path d="M 45 145 A 27 27 0 0 1 45 199"/><path d="M 578 145 A 27 27 0 0 0 578 199"/><path d="M 132 132 A 40 40 0 0 0 132 212 M 491 132 A 40 40 0 0 1 491 212" stroke-dasharray="9 7"/></g>`;
  root.innerHTML=`<svg class="court-plot court-full" viewBox="0 0 623 345" role="img" aria-label="Quadra horizontal com ${shots.length} arremessos identificados"><title>${shots.length} arremessos com coordenadas disponíveis</title>${court}${markers}</svg><p class="chart-key">${shots.length} com posição de ${quarterShots(c,t).length} tentativas identificadas: ${shots.filter(sh=>sh[4]).length} convertidos e ${shots.filter(sh=>!sh[4]).length} não convertidos. As posições são percentuais do gráfico original da LNB e não foram espelhadas.</p>`;
}
function percentBars(id,items,maximum){
 const root=$(id);root.replaceChildren();root.className='bars';
 if(!items.length){const empty=document.createElement('div');empty.className='empty';empty.textContent='Ainda não há dados disponíveis para este recorte.';root.append(empty);return}
 items.forEach((item,index)=>{const row=document.createElement('div');row.className='bar-row';const label=document.createElement('span');label.className='bar-name';label.textContent=item.name;const track=document.createElement('div');track.className='track';const fill=document.createElement('div');fill.className='fill';fill.style.width=Math.max(0,Math.min(100,100*item.value/maximum))+'%';if(index%2)fill.style.background='#75ced5';track.append(fill);const value=document.createElement('span');value.className='value';value.textContent=item.text;row.append(label,track,value);root.append(row)});
}
function renderShotMix(data){
 const root=$('advanced-shot-mix');const players=data.sample.players.map(p=>({name:p.name,two:Number(p.two)||0,three:Number(p.three)||0})).filter(p=>p.two+p.three>0).sort((a,b)=>(b.two+b.three)-(a.two+a.three)).slice(0,8);
 if(!players.length){root.innerHTML='<div class="empty">Nenhuma tentativa individual validada neste recorte.</div>';return}
 root.innerHTML=players.map(p=>{const total=p.two+p.three;return `<div class="mix-row" aria-label="${esc(p.name)}: ${p.two} tentativas de 2 pontos e ${p.three} tentativas de 3 pontos"><span>${esc(p.name)}</span><span class="mix-track" aria-hidden="true"><span class="mix-two" style="width:${100*p.two/total}%"></span><span class="mix-three" style="width:${100*p.three/total}%"></span></span><span class="mix-values">${p.two} de 2 · ${p.three} de 3</span></div>`}).join('')+'<p class="chart-key">Cada barra representa 100% das tentativas do atleta; considere a diferença de volume entre atletas.</p>';
}
function renderGameEfg(c,t,games){
 const rows=[];for(const g of games){const totals=totalsForAnalysis(c,t,[g]),attempts=totals.attempts;if(!attempts)continue;const efg=totals.efg,side=names(g,c).indexOf(t);rows.push({name:names(g,c)[1-side]+' · '+(g.date?g.date.slice(5).split('-').reverse().join('/'):'—')+' · n='+attempts,value:100*efg,text:formatPercent(efg)})}
 percentBars('advanced-game-efg',rows.slice(0,8),150);
}

function renderAdvancedPeriods(c,t){
  if(c.type!=='nbb'){bars('advanced-periods',[]);bars('advanced-period-accuracy',[]);const note=document.createElement('p');note.className='small muted';note.textContent='As súmulas CBI disponíveis não separam arremessos por quarto.';$('advanced-periods').append(note);return}
  const counts=new Map();for(const {shot} of quarterShots(c,t,true)){const p=shot[2]>=5?'Prorrogações':`${shot[2]}º quarto`,v=counts.get(p)||{attempts:0,made:0};v.attempts++;v.made+=Number(shot[4]||0);counts.set(p,v)}
  const sorted=[...counts].sort((a,b)=>a[0].localeCompare(b[0],'pt-BR'));
  bars('advanced-periods',sorted.map(([name,v])=>({name,value:v.attempts,text:String(v.attempts)})));
  percentBars('advanced-period-accuracy',sorted.map(([name,v])=>({name:name+' · n='+v.attempts,value:100*v.made/v.attempts,text:fmt(100*v.made/v.attempts)+'%'})),100);
}

function renderAdvancedTrend(c,t,games){
 const root=$('advanced-trend'), series=[...games].sort((a,b)=>(a.date||'').localeCompare(b.date||'')).slice(-12);
 if(!series.length){root.innerHTML='<div class="empty">Ainda não há resultados finais neste recorte.</div>';return}
 const points=series.map(g=>{const side=names(g,c).indexOf(t),scores=score(g,c);return {date:g.date||'',for:Number(scores[side]),against:Number(scores[1-side]),opponent:names(g,c)[1-side]}});
 const max=Math.ceil(Math.max(10,...points.flatMap(x=>[x.for,x.against]))*1.1),width=760,height=220,left=42,right=20,top=16,bottom=32;
 const px=i=>left+(points.length===1?(width-left-right)/2:i*(width-left-right)/(points.length-1));
 const py=v=>top+(height-top-bottom)*(1-v/max);
 const line=key=>points.map((v,i)=>`${px(i).toFixed(1)},${py(v[key]).toFixed(1)}`).join(' ');
 const dots=key=>points.map((v,i)=>`<circle cx="${px(i).toFixed(1)}" cy="${py(v[key]).toFixed(1)}" r="3.5" fill="${key==='for'?'#ff875e':'#75ced5'}"><title>${esc(v.date)} · ${esc(v.opponent)} · ${key==='for'?'marcados':'sofridos'}: ${v[key]}</title></circle>`).join('');
 const first=points[0].date,last=points[points.length-1].date;
 root.innerHTML=`<svg class="court-plot" viewBox="0 0 ${width} ${height}" role="img" aria-label="Evolução de pontos marcados e sofridos em ${points.length} partidas"><line x1="${left}" x2="${width-right}" y1="${height-bottom}" y2="${height-bottom}" stroke="#8798aa"/><line x1="${left}" x2="${left}" y1="${top}" y2="${height-bottom}" stroke="#8798aa"/><text x="5" y="${top+6}" fill="#b2c0cf" font-size="12">${Math.ceil(max)}</text><text x="23" y="${height-bottom}" fill="#b2c0cf" font-size="12">0</text><polyline points="${line('for')}" fill="none" stroke="#ff875e" stroke-width="3"/><polyline points="${line('against')}" fill="none" stroke="#75ced5" stroke-width="3" stroke-dasharray="7 4"/>${dots('for')}${dots('against')}<text x="${left}" y="${height-7}" fill="#b2c0cf" font-size="12">${esc(first)}</text><text x="${width-right}" y="${height-7}" text-anchor="end" fill="#b2c0cf" font-size="12">${esc(last)}</text></svg><p class="chart-key">Laranja contínuo: marcados · Azul tracejado: sofridos · eixo vertical: pontos.</p><details><summary>Ver valores por jogo</summary><div class="table-wrap"><table><thead><tr><th>Data</th><th>Adversário</th><th class="num">Marcados</th><th class="num">Sofridos</th></tr></thead><tbody>${points.map(v=>`<tr><td>${esc(v.date)}</td><td>${esc(v.opponent)}</td><td class="num">${v.for}</td><td class="num">${v.against}</td></tr>`).join('')}</tbody></table></div></details>`;
}
function renderTactical(c,t,data){
 const recent=data.games.slice(0,8).map(g=>{const i=names(g,c).indexOf(t),s=score(g,c),margin=Number(s[i])-Number(s[1-i]);return{name:names(g,c)[1-i]+' · '+(g.date||'—'),value:Math.abs(margin),text:(margin>0?'+':'')+margin+' pts'}});
 bars('tactical-margins',recent);
 const panel=$('cbi-tactical-panel'),source=$('cbi-scoring-panel');panel.hidden=source.hidden=c.type!=='cbi';if(c.type!=='cbi')return;
 const players=data.sample.players.filter(p=>Number(p.points)>0).sort((a,b)=>b.points-a.points),total=players.reduce((a,p)=>a+p.points,0);
 bars('cbi-points-distribution',players.slice(0,10).map(p=>({name:p.name,value:p.points,text:fmt(100*p.points/total)+'% · '+p.points+' pts'})));
 const top=players.slice(0,2).reduce((a,p)=>a+p.points,0);
 $('cbi-points-summary').textContent=total?`Até dois atletas concentram ${fmt(100*top/total)}% dos ${total} pontos registrados em ${data.sample.covered} de ${data.games.length} súmula(s) da equipe. Cobertura parcial pode alterar a interpretação.`:`Não há pontos individuais disponíveis nas súmulas coletadas para esta equipe (${data.sample.covered} de ${data.games.length} jogos).`;
 const made=key=>data.sample.players.reduce((a,p)=>a+(Number(p[key])||0),0),twos=made('scoredTwo'),threes=made('scoredThree'),ft=made('scoredFt'),known=2*twos+3*threes+ft;
 $('cbi-shot-source').innerHTML=known?`<p>Dos ${total} pontos das súmulas, ${known} foram associados a cestas individuais conferidas. A fatia de cada origem usa somente esses ${known} pontos.</p><div class="table-wrap"><table><thead><tr><th>Origem</th><th class="num">Cestas convertidas</th><th class="num">Pontos</th><th class="num">Fatia</th></tr></thead><tbody>`+[["2 pontos",twos,2*twos],["3 pontos",threes,3*threes],["Lances livres",ft,ft]].map(([label,n,pts])=>`<tr><td>${label}</td><td class="num">${n}</td><td class="num">${pts}</td><td class="num">${fmt(100*pts/known)}%</td></tr>`).join('')+'</tbody></table></div>':'<div class="empty">Nenhuma origem da pontuação individual foi validada nas súmulas coletadas.</div>';
 const covered=data.games.filter(g=>g.boxscore?.[names(g,c).indexOf(t)===0?'home':'away']).sort((a,b)=>(b.date||'').localeCompare(a.date||''));
 if(covered.length<6){$('cbi-recent-explanation').textContent=`São necessárias pelo menos 6 súmulas individuais da equipe: 3 recentes e 3 anteriores. Há ${covered.length} disponível(is).`; $('cbi-recent-table').innerHTML='<tr><td colspan="4">Amostra insuficiente para o ajuste.</td></tr>';return}
 const collect=games=>{const m=new Map();let sum=0;for(const g of games){const box=g.boxscore[names(g,c).indexOf(t)===0?'home':'away'];for(const p of box.players||[]){const points=Number(p.stats?.points);if(!p.id||!Number.isFinite(points)||points<0)continue;const id=String(p.id),v=m.get(id)||{name:p.name,points:0};v.points+=points;m.set(id,v);sum+=points}}return{m,sum}};
 const latest=collect(covered.slice(0,3)),prior=collect(covered.slice(3));if(!latest.sum||!prior.sum){$('cbi-recent-explanation').textContent='Não há pontos suficientes nas súmulas para calcular o ajuste.';$('cbi-recent-table').innerHTML='<tr><td colspan="4">Sem amostra de pontuação.</td></tr>';return}
 const priorWeight=3*prior.sum/(covered.length-3),ids=new Set([...latest.m.keys(),...prior.m.keys()]);const rows=[...ids].map(id=>{const a=latest.m.get(id),b=prior.m.get(id),recent=(a?.points||0)/latest.sum,reference=(b?.points||0)/prior.sum;return{name:a?.name||b.name,recent,reference,adjusted:((a?.points||0)+priorWeight*reference)/(latest.sum+priorWeight)}}).sort((a,b)=>b.adjusted-a.adjusted).slice(0,12);
 $('cbi-recent-explanation').textContent=`As 3 súmulas mais recentes são combinadas com o perfil das ${covered.length-3} anteriores, que recebem peso equivalente a 3 jogos médios. As porcentagens representam participação na pontuação, não probabilidade de arremessar nem previsão de desempenho; escalações e adversários variam e uma ausência conta como zero pontos.`;
 $('cbi-recent-table').innerHTML=rows.map(r=>`<tr><td>${esc(r.name)}</td><td class="num">${formatPercent(r.recent)}</td><td class="num">${formatPercent(r.reference)}</td><td class="num">${formatPercent(r.adjusted)}</td></tr>`).join('');
}

function renderAdvancedComparison(){
 const c=selectedCompetition(),a=team.value,b=compareControl.value;if(!c||!a||!b)return;
 const one=totalsForAnalysis(c,a),two=totalsForAnalysis(c,b),oneScore=statsFor(c,a),twoScore=statsFor(c,b);
 const row=(name,x,y)=>'<tr><td>'+esc(name)+'</td><td class="num">'+esc(x)+'</td><td class="num">'+esc(y)+'</td></tr>';
 $('advanced-comparison').innerHTML='<div class="table-wrap"><table><thead><tr><th>Indicador</th><th class="num">'+esc(a)+'</th><th class="num">'+esc(b)+'</th></tr></thead><tbody>'+row('Jogos finalizados',one.games.length,two.games.length)+row('Campanha (vitórias–derrotas)',oneScore.w+'–'+oneScore.l,twoScore.w+'–'+twoScore.l)+row('Pontos marcados / jogo',fmt(oneScore.pf/one.games.length),fmt(twoScore.pf/two.games.length))+row('Pontos sofridos / jogo',fmt(oneScore.pa/one.games.length),fmt(twoScore.pa/two.games.length))+row('eFG% · amostra de arremessos',formatPercent(one.efg),formatPercent(two.efg))+row('Tentativas registradas',one.attempts,two.attempts)+row('Jogos com dados de equipe',one.teamCovered,two.teamCovered)+'</tbody></table></div><div class="grid"><div class="chart-pair"><h4>eFG% entre equipes</h4><div id="compare-efg"></div></div><div class="chart-pair"><h4>Frequência de arremessos de 3</h4><div id="compare-three"></div></div></div>';
 percentBars('compare-efg',[[a,one],[b,two]].filter(([,d])=>d.efg!==null).map(([name,d])=>({name:name+' · n='+d.attempts,value:100*d.efg,text:formatPercent(d.efg)})),150);
 percentBars('compare-three',[[a,one],[b,two]].filter(([,d])=>d.threeRate!==null).map(([name,d])=>({name:name+' · n='+d.attempts,value:100*d.threeRate,text:formatPercent(d.threeRate)})),100);
 const direct=c.games.filter(g=>{const ns=names(g,c);return ns.includes(a)&&ns.includes(b)}).sort((x,y)=>(y.date||'').localeCompare(x.date||''));
 $('advanced-h2h').innerHTML=direct.length?direct.map(g=>gameCard(g,c,a,false)).join(''):'<div class="empty">Não há confronto direto entre essas equipes na amostra selecionada.</div>';
}
function renderMarkovDemo(){
 const labels=['Início da posse','Circulação no perímetro','Infiltração','Jogo interno','Arremesso de 3','Meia distância','Finalização próxima','Rebote ofensivo'];
 const entries=Object.entries(markovDemo.state_epv||{});
 const prob=(object,key)=>Number.isFinite(object?.[key])?fmt(object[key]*100)+'%':'—';
 const rows=entries.map(([key,value],i)=>'<tr><td>'+esc(labels[i]||key)+'</td><td class="num">'+fmt2(value)+'</td><td class="num">'+fmt2(markovDemo.steps_to_absorption[key])+'</td></tr>').join('');
 const outcomes=entries.map(([key],i)=>{const v=markovDemo.absorption_probabilities?.[key];return '<tr><td>'+esc(labels[i]||key)+'</td><td class="num">'+prob(v,'A1_Made_2PT')+'</td><td class="num">'+prob(v,'A2_Made_3PT')+'</td><td class="num">'+prob(v,'A3_Made_FT')+'</td><td class="num">'+prob(v,'A4_Turnover')+'</td><td class="num">'+prob(v,'A5_Def_Rebound')+'</td></tr>'}).join('');
 $('markov-demo').innerHTML='<div class="table-wrap"><table><thead><tr><th>Estado hipotético</th><th class="num">EPV · pontos esperados</th><th class="num">Ações médias até o desfecho</th></tr></thead><tbody>'+rows+'</tbody></table></div><p class="small">Estados e transições são parâmetros ilustrativos. Abaixo, cada célula indica a probabilidade de um desfecho segundo o modelo de exemplo.</p><div class="table-wrap"><table><thead><tr><th>Estado inicial</th><th class="num">Cesta de 2</th><th class="num">Cesta de 3</th><th class="num">Lance livre</th><th class="num">Perda de bola</th><th class="num">Rebote defensivo</th></tr></thead><tbody>'+outcomes+'</tbody></table></div>';
}

compareControl.addEventListener('change',renderAdvancedComparison);
$('map-result').addEventListener('change',()=>{const c=selectedCompetition();if(c&&team.value)renderAdvancedMap(c,team.value)});
for(const control of [comp,team,$('quarter'),$('shot-type')])control.addEventListener('change',renderAdvanced);
renderMarkovDemo();
if(competitions.length)renderAdvanced();
