const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
const template = fs.readFileSync('cbb/export/templates/dashboard.html', 'utf8');
const app = 'const nbb=' + template.split('<script>\nconst nbb=')[1].split('</script>')[0];
const advanced = fs.readFileSync('cbb/export/templates/advanced_analytics.js', 'utf8');
const games=[];
for(let i=0;i<3;i++) {
  const shots=[];
  for(let j=0;j<6;j++)shots.push([0,'p1',1,2,1,25,40]);
  for(let j=0;j<4;j++)shots.push([0,'p2',1,3,0,65,30]);
  shots.push([0,'p1',2,2,1,20,40]);
  for(let j=0;j<3;j++)shots.push([0,'p2',2,3,0,60,30]);
  games.push({id:String(i),season:'2026-2027',date:`2026-10-0${i+1}`,teams:['A','B'],score:[70,60],url:'https://example.org/game',players:{p1:'Ana',p2:'Bia'},shots});
}
const player=(id,name,points,fgm,fga,tpm,tpa,ftm,fta)=>({id,name,stats:{points,game_played:1,field_goals_made:fgm,field_goals_attempted:fga,three_point_field_goals_made:tpm,three_point_field_goals_attempted:tpa,free_throws_made:ftm,free_throws_attempted:fta}});
const cbigame={id:'c1',date:'2026-09-01',home_team:'A',away_team:'B',home_score:8,away_score:6,is_finished:true,url:'https://example.org/c1',boxscore:{home:{players:[player('x','Alice',8,2,4,1,3,1,2)]},away:{players:[player('y','Bea',6,3,5,0,1,0,0)]}}};
const cbi={competitions:[{id:'completed',name:'CBI final',games:[cbigame]},{id:'future',name:'CBI futuro',games:[{id:'future',is_finished:false}]}]};
const model={state_epv:{S0_Trans_Inflow:1.17},steps_to_absorption:{S0_Trans_Inflow:3.71},absorption_probabilities:{S0_Trans_Inflow:{A1_Made_2PT:0.4,A2_Made_3PT:0.1,A3_Made_FT:0.1,A4_Turnover:0.2,A5_Def_Rebound:0.2}}};
class Element {
 constructor(id=''){this.id=id;this.children=[];this.handlers={};this.value='';this.textContent='';this.innerHTML='';this.dataset={};this.style={};this.hidden=false}
 get options(){return this.children}
 replaceChildren(...v){this.children=v;if(['competition','team','compare-team'].includes(this.id))this.value=v[0]?.value||''}
 append(...v){this.children.push(...v)}
 addEventListener(event,fn){(this.handlers[event]??=[]).push(fn)}
 fire(event){for(const fn of this.handlers[event]||[])fn({key:''})}
 setAttribute(name,value){this[name]=value}
 focus(){}
}
const elements={}; const el=id=>elements[id]||(elements[id]=new Element(id));
el('nbb-observed-data').textContent=JSON.stringify({games});el('cbi-observed-data').textContent=JSON.stringify(cbi);el('markov-demo-data').textContent=JSON.stringify(model);el('quarter').value='0';el('shot-type').value='0';
const tabs=['team','analysis','players','games','method'].map(v=>{const e=new Element();e.dataset.view=v;return e});
const views=['team','analysis','players','games','method'].map(v=>new Element('view-'+v));
const document={getElementById:el,createElement:()=>new Element(),querySelectorAll:q=>q==='.tabs button'?tabs:q==='.view'?views:[]};
function Option(text,value){this.textContent=text;this.value=value}
const ctx=vm.createContext({document,Option,Intl,console});vm.runInContext(app,ctx);vm.runInContext(advanced,ctx);
assert.strictEqual(el('competition').value,'nbb:2026-2027');
assert(!vm.runInContext('competitions',ctx).some(c=>c.id==='cbi:future'));
assert(el('advanced-cards').innerHTML.includes('eFG%'));
assert(el('advanced-map').innerHTML.includes('42 arremessos'));
el('quarter').value='1';el('quarter').fire('change');
assert(el('advanced-map').innerHTML.includes('30 arremessos'));
assert(el('advanced-shrinkage').textContent.includes('20 tentativas equivalentes'));
assert(el('advanced-distribution-table').innerHTML.includes('46,0%'));
assert(el('advanced-distribution-table').innerHTML.includes('54,0%'));
el('quarter').value='3';el('quarter').fire('change');
assert(el('advanced-shrinkage').textContent.includes('indisponível'));
assert(el('advanced-map').innerHTML.includes('Sem coordenadas'));
el('competition').value='cbi:completed';el('competition').fire('change');
assert.strictEqual(el('team').value,'A');
const metrics=vm.runInContext("totalsForAnalysis(selectedCompetition(), team.value)",ctx);
assert.strictEqual(metrics.attempts,7);
assert(Math.abs(metrics.efg-.5)<1e-10);
assert(Math.abs(metrics.ftr-2/7)<1e-10);
assert(Math.abs(metrics.ts-8/(2*(7+0.44*2)))<1e-10);
assert(el('advanced-map').innerHTML.includes('não fornece coordenadas'));
assert(el('markov-demo').innerHTML.includes('Perda de bola'));
tabs[1].fire('click');assert.strictEqual(views.find(v=>v.id==='view-analysis').hidden,false);
console.log('OK: indicadores, comparação, mapa, ajuste por período, CBI e modelo demonstrativo');
