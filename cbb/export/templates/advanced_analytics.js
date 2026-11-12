/* Advanced analysis uses the current competition and team; no sample data is mixed in. */
const markovDemo = JSON.parse($('markov-demo-data').textContent);
const compareControl = $('compare-team');
const fmt2=value=>new Intl.NumberFormat('pt-BR',{minimumFractionDigits:2,maximumFractionDigits:2}).format(value);
let comparisonCompetition = '';
function totalsForAnalysis(c,t) {
  const games=teamGames(c,t), sample=playerData(c,t,games);
  const sum=key=>sample.players.reduce((a,p)=>a+(Number(p[key])||0),0);
  const two=sum('two'),three=sum('three'),twoMade=sum('twoMade'),threeMade=sum('threeMade');
  const attempts=two+three, ft=c.type==='cbi'?sum('ft'):null, validPoints=c.type==='cbi'?sum('validPoints'):null;
  return {games,sample,two,three,twoMade,threeMade,attempts,ft,
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
  $('advanced-coverage').textContent=`Amostra: ${data.attempts} tentativas de quadra em ${s.covered} de ${data.games.length} jogo(s) da equipe com ${c.type==='nbb'?'arremessos identificados':'súmulas individuais conferidas'}. `+(c.type==='cbi'?'Os arremessos usam apenas linhas que também passam pela validação individual; a cobertura pode variar por atleta.':'A fonte não contém todos os jogos da competição. O FTR não está disponível nos registros de arremesso.');
  renderAdvancedDistribution(c,t,data);
  renderAdvancedMap(c,t);
  renderAdvancedPeriods(c,t);
  renderAdvancedTrend(c,t,data.games);
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
  $('advanced-shrinkage').textContent=adjusted?`Fatia ajustada: combina ${total} tentativas em ${sampleGames} jogos com 20 tentativas equivalentes distribuídas conforme os ${priorTotal} arremessos dos outros períodos. É uma descrição histórica, não previsão de acionamento.`:(c.type==='nbb'&&q?'Fatia ajustada indisponível: exige pelo menos 20 tentativas em três jogos no período selecionado e referência em outros períodos.':'Selecione um período no NBB para avaliar a fatia ajustada; o ajuste requer amostra mínima. O CBI ainda não fornece esse recorte na base.');
  $('advanced-distribution-table').innerHTML=players.length?players.map(p=>'<tr><td>'+esc(p.name)+'</td><td class="num">'+p.attempts+'</td><td class="num">'+formatPercent(p.share)+'</td><td class="num">'+formatPercent(p.adjusted)+'</td></tr>').join(''):'<tr><td colspan="4">Nenhuma tentativa identificada neste recorte.</td></tr>';
}
function renderAdvancedMap(c,t){
  const root=$('advanced-map');if(c.type!=='nbb'){root.innerHTML='<div class="empty">A fonte CBI desta base ainda não fornece coordenadas dos arremessos. Consulte as súmulas individuais na aba Jogos.</div>';return}
  const shots=quarterShots(c,t).map(x=>x.shot).filter(sh=>sh[5]!==null&&sh[5]!==undefined&&sh[6]!==null&&sh[6]!==undefined&&Number.isFinite(Number(sh[5]))&&Number.isFinite(Number(sh[6]))&&sh[5]>=0&&sh[5]<=100&&sh[6]>=0&&sh[6]<=100);
  if(!shots.length){root.innerHTML='<div class="empty">Sem coordenadas disponíveis neste recorte.</div>';return}
  const markers=shots.map(sh=>{const x=Number(sh[5]),y=Number(sh[6]);return sh[4]?`<circle cx="${x}" cy="${y}" r="1.1" fill="#75ced5" opacity=".75"><title>Convertido · ${sh[3]} pontos</title></circle>`:`<path d="M ${x-1} ${y-1} L ${x+1} ${y+1} M ${x+1} ${y-1} L ${x-1} ${y+1}" stroke="#ff875e" stroke-width=".65"><title>Não convertido · ${sh[3]} pontos</title></path>`}).join('');
  root.innerHTML=`<svg class="court-plot" viewBox="0 0 100 100" role="img" aria-label="Mapa relativo de ${shots.length} arremessos identificados"><title>${shots.length} arremessos com coordenadas disponíveis</title><rect x="0" y="0" width="100" height="100" fill="#14202d"/>${markers}</svg><p class="chart-key">${shots.length} com posição de ${quarterShots(c,t).length} tentativas identificadas: ${shots.filter(sh=>sh[4]).length} convertidos e ${shots.filter(sh=>!sh[4]).length} não convertidos · eixos de 0 a 100% conforme o relatório.</p>`;
}
function renderAdvancedPeriods(c,t){
  if(c.type!=='nbb'){bars('advanced-periods',[]);const note=document.createElement('p');note.className='small muted';note.textContent='As súmulas CBI disponíveis não separam arremessos por quarto.';$('advanced-periods').append(note);return}
  const counts=new Map();for(const {shot} of quarterShots(c,t,true)){const p=shot[2]>=5?'Prorrogações':`${shot[2]}º quarto`;counts.set(p,(counts.get(p)||0)+1)}
  bars('advanced-periods',[...counts].sort((a,b)=>a[0].localeCompare(b[0],'pt-BR')).map(([name,value])=>({name,value,text:String(value)})));
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
function renderAdvancedComparison(){
 const c=selectedCompetition(),a=team.value,b=compareControl.value;if(!c||!a||!b)return;
 const one=totalsForAnalysis(c,a),two=totalsForAnalysis(c,b),oneScore=statsFor(c,a),twoScore=statsFor(c,b);
 const row=(name,x,y)=>'<tr><td>'+esc(name)+'</td><td class="num">'+esc(x)+'</td><td class="num">'+esc(y)+'</td></tr>';
 $('advanced-comparison').innerHTML='<div class="table-wrap"><table><thead><tr><th>Indicador</th><th class="num">'+esc(a)+'</th><th class="num">'+esc(b)+'</th></tr></thead><tbody>'+row('Jogos finalizados',one.games.length,two.games.length)+row('Campanha (vitórias–derrotas)',oneScore.w+'–'+oneScore.l,twoScore.w+'–'+twoScore.l)+row('Pontos marcados / jogo',fmt(oneScore.pf/one.games.length),fmt(twoScore.pf/two.games.length))+row('Pontos sofridos / jogo',fmt(oneScore.pa/one.games.length),fmt(twoScore.pa/two.games.length))+row('eFG% · amostra de arremessos',formatPercent(one.efg),formatPercent(two.efg))+row('Tentativas registradas',one.attempts,two.attempts)+row('Jogos com registros',one.sample.covered,two.sample.covered)+'</tbody></table></div>';
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
for(const control of [comp,team,$('quarter'),$('shot-type')])control.addEventListener('change',renderAdvanced);
renderMarkovDemo();
if(competitions.length)renderAdvanced();
