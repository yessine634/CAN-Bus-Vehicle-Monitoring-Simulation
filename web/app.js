const $ = id => document.getElementById(id);
const metrics = [
  ['speed','Vehicle speed','km/h','0x100',100,'Limit · 100 km/h'],
  ['rpm','Engine RPM','RPM','0x100',4000,'Limit · 4,000 RPM'],
  ['engine_temp','Engine temperature','°C','0x101',100,'Limit · 100 °C'],
  ['battery_voltage','Battery voltage','V','0x200',null,'Low voltage · below 11 V'],
  ['battery_current','Battery current','A','0x200',null,'Battery load'],
  ['battery_temp','Battery temperature','°C','0x201',45,'Limit · 45 °C']
];
for(const [key,label,unit,id,,note] of metrics){
  const card=document.createElement('article');card.className='metric';card.id=`card-${key}`;
  card.innerHTML=`<div class="metric-top"><span>${label}</span><code>${id}</code></div><div class="reading"><span id="value-${key}">—</span><small>${unit}</small></div><div class="metric-note">${note}</div><svg id="chart-${key}" viewBox="0 0 300 70" preserveAspectRatio="none" role="img" aria-label="${label} trend"></svg>`;
  $('metrics').append(card);
}
let pending=false, plotSignature='';
function sparkline(id, values, warning){
  const svg=$(id);if(values.length<2){svg.innerHTML='<line x1="0" y1="55" x2="300" y2="55" stroke="#e6ece2" stroke-dasharray="4 4"/>';return;}
  const samples=values.slice(-150), low=Math.min(...samples), high=Math.max(...samples), range=high-low||1;
  const pts=samples.map((v,i)=>`${(i/(samples.length-1)*300).toFixed(2)},${(55-(v-low)/range*43).toFixed(2)}`).join(' ');
  const color=warning?'#d58a55':'#4b9a7f';
  svg.innerHTML=`<polygon points="0,70 ${pts} 300,70" fill="${color}" opacity=".09"/><polyline points="${pts}" fill="none" stroke="${color}" stroke-width="2" vector-effect="non-scaling-stroke"/>`;
}
function render(s){
  const active=['running','stopping'].includes(s.status);
  $('start').disabled=pending||active;$('stop').disabled=pending||!active||s.status==='stopping';$('duration').disabled=active;
  const labels={idle:'Ready to simulate',running:'Simulation live',stopping:'Finishing & saving',completed:'Run completed',error:'Simulation failed'};
  $('status').textContent=`● ${labels[s.status]}`;$('status').className=`status ${s.status}`;
  $('messages').innerHTML=`${s.rows} <small>messages</small>`;
  $('fault-total').innerHTML=`${s.fault_count} <small>detected</small>`;
  $('fault-note').textContent=s.fault_count?`${Object.keys(s.counts).length} fault types recorded`:active?'No fault events recorded yet':'Waiting for a simulation';
  $('elapsed').innerHTML=`${s.elapsed.toFixed(1)} <small>/ ${s.duration} s</small>`;
  $('phase').textContent=active?(s.elapsed>=s.duration?'Generating graphs & diagnostic summary…':'Receiving messages from virtual ECUs'):s.status==='completed'?'Complete · reports ready':s.status==='error'?'Open the console for error details':'Start a run to receive live readings';
  $('progress').style.width=`${s.status==='completed'?100:Math.min(s.elapsed/s.duration*100,100)}%`;
  for(const [key,,unit,,limit] of metrics){
    const value=s.latest[key],warning=value!==undefined&&(key==='battery_voltage'?value<11:limit!==null&&value>limit);
    $(`value-${key}`).textContent=value===undefined?'—':unit==='V'?value.toFixed(1):Math.round(value).toLocaleString();
    $(`card-${key}`).classList.toggle('warning',warning);sparkline(`chart-${key}`,s.history[key]||[],warning);
  }
  const brake=s.latest.brake_status;
  $('brake-label').textContent=brake===undefined?'Awaiting signal':['System normal','Brake applied','Brake system fault'][brake];
  $('brake-detail').textContent=brake===undefined?'Brake system status will appear when the first frame arrives.':brake===2?'C001 · Critical brake fault detected in the latest frame.':brake===1?'The latest frame indicates active braking.':'The latest frame reports normal brake operation.';
  $('brake-symbol').style.color=brake===2?'#be4d3c':brake===1?'#dc773d':'#147d67';
  $('fault-badge').textContent=`${s.fault_count} events`;
  const tbody=$('fault-rows');tbody.replaceChildren();
  if(!s.faults.length){const tr=tbody.insertRow();const td=tr.insertCell();td.colSpan=4;td.className='empty';td.textContent=s.status==='completed'?'Run completed without detected faults.':'No events yet. Start a simulation to inspect vehicle faults.';}
  for(const fault of s.faults){const tr=tbody.insertRow();for(const key of ['timestamp','fault_code','priority','message']){const td=tr.insertCell();if(key==='priority'){const badge=document.createElement('span');badge.className=`severity ${fault.priority}`;badge.textContent=fault[key];td.append(badge);}else td.textContent=key==='timestamp'?fault[key].split(' ')[1]:fault[key];}}
  $('output').textContent=s.output||'Ready. Start a simulation to see its output.';
  $('download').hidden=!s.rows;
  $('report-hint').textContent=s.status==='completed'?'Run complete. Open a graph to inspect it, or download the full CSV log.':active?'Graphs will appear here once the simulation finishes saving its data.':'At the end of a run, the simulator generates six graphs and a diagnostic summary.';
  const signature=JSON.stringify([s.run_id,s.plots]);
  if(signature!==plotSignature){plotSignature=signature;$('plots').replaceChildren();for(const filename of s.plots){const a=document.createElement('a');a.href=`/plots/${encodeURIComponent(filename)}?run=${s.run_id}`;a.target='_blank';a.rel='noopener';const img=document.createElement('img');img.src=a.href;img.alt=filename.replaceAll('_',' ').replace('.png','');img.loading='lazy';const caption=document.createElement('span');caption.textContent=img.alt+' ↗';a.append(img,caption);$('plots').append(a);}}
  if(s.status==='error'){$('error').hidden=false;$('error').textContent='The simulation could not finish. Expand the console below for details.';}
}
async function refresh(){try{const response=await fetch('/api/state',{cache:'no-store'});if(!response.ok)throw Error('Could not read the simulator state.');render(await response.json());}catch(error){$('error').hidden=false;$('error').textContent='Connection lost. Make sure dashboard.cmd is running.';}}
async function action(path){if(pending)return;pending=true;$('start').disabled=true;$('stop').disabled=true;$('error').hidden=true;try{const response=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json','X-Dashboard':'1'},body:JSON.stringify({duration:Number($('duration').value)})});const data=await response.json();if(!response.ok)throw Error(data.error||'Request failed.');}catch(error){$('error').hidden=false;$('error').textContent=error.message;}finally{pending=false;await refresh();}}
$('start').onclick=()=>action('/api/start');$('stop').onclick=()=>action('/api/stop');
(async function poll(){await refresh();setTimeout(poll,500);})();
