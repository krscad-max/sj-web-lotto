// Simple client-side lotto helper
const dataUrls = {
  '649':'data/lotto_649.csv',
  'max':'data/lotto_max.csv'
}
let cache = {}

async function loadData(game){
  if(cache[game]) return cache[game]
  const res = await fetch(dataUrls[game])
  const txt = await res.text()
  const rows = txt.trim().split('\n').map(r=>r.trim()).filter(Boolean)
  // expected: date, n1,n2,... format
  const parsed = rows.map(r=>{
    const parts=r.split(',').map(s=>s.trim())
    return {date:parts[0], nums:parts.slice(1).map(x=>parseInt(x,10)).filter(n=>!isNaN(n))}
  })
  cache[game]=parsed
  return parsed
}

function freqStrategy(history,want){
  const cnt = {}
  history.forEach(h=>h.nums.forEach(n=>cnt[n]=(cnt[n]||0)+1))
  const sorted = Object.keys(cnt).map(n=>[parseInt(n),cnt[n]]).sort((a,b)=>b[1]-a[1])
  return sorted.slice(0,want).map(x=>x[0])
}

function randomWeighted(history,want){
  // simple: weight by frequency + small randomness
  const cnt = {}
  history.forEach(h=>h.nums.forEach(n=>cnt[n]=(cnt[n]||0)+1))
  const pool = []
  for(let i=1;i<=50;i++){
    const w = (cnt[i]||0)+1
    for(let j=0;j<w;j++) pool.push(i)
  }
  const out=[]
  while(out.length<want && pool.length){
    const pick = pool[Math.floor(Math.random()*pool.length)]
    if(!out.includes(pick)) out.push(pick)
  }
  return out
}

function balancedStrategy(history,want){
  // try to balance odd/even
  let set=[]
  while(set.length<want){
    const candidate = Math.floor(Math.random()*49)+1
    if(!set.includes(candidate)) set.push(candidate)
  }
  // ensure roughly half odd/even
  return set
}

function renderHistory(tableEl,history){
  let html = '<table><thead><tr><th>Date</th><th>Numbers</th></tr></thead><tbody>'
  history.slice(0,200).forEach(h=>{
    html += `<tr><td>${h.date}</td><td>${h.nums.join(', ')}</td></tr>`
  })
  html += '</tbody></table>'
  tableEl.innerHTML = html
}

function downloadCSV(arr){
  const lines = arr.map(a=>a.join(','))
  const blob = new Blob([lines.join('\n')],{type:'text/csv'})
  const url = URL.createObjectURL(blob)
  const a=document.createElement('a');a.href=url;a.download='lotto_sets.csv';a.click();URL.revokeObjectURL(url)
}

async function main(){
  const gameSelect=document.getElementById('gameSelect')
  const strategy=document.getElementById('strategy')
  const genBtn=document.getElementById('genBtn')
  const output=document.getElementById('output')
  const historyTable=document.getElementById('historyTable')
  const countInput=document.getElementById('count')
  const exportCsv=document.getElementById('exportCsv')
  let lastSets=[]

  async function refreshHistory(){
    const game = gameSelect.value
    const hist = await loadData(game)
    renderHistory(historyTable,hist)
    return hist
  }

  await refreshHistory()

  genBtn.addEventListener('click', async ()=>{
    const game = gameSelect.value
    const strat = strategy.value
    const want = game==='max'?7:6
    const hist = await loadData(game)
    const sets = []
    const howMany = Math.max(1,Math.min(20,parseInt(countInput.value)||5))
    for(let i=0;i<howMany;i++){
      let s
      if(strat==='random') s = randomWeighted(hist,want)
      else if(strat==='freq') s = freqStrategy(hist,want)
      else if(strat==='cold'){
        // pick numbers with lowest counts
        const cnt={}
        hist.forEach(h=>h.nums.forEach(n=>cnt[n]=(cnt[n]||0)+1))
        const sorted = Array.from({length:50},(_,i)=>i+1).sort((a,b)=>(cnt[a]||0)-(cnt[b]||0))
        s = sorted.slice(0,want)
      } else s = balancedStrategy(hist,want)
      sets.push(s.sort((a,b)=>a-b))
    }
    lastSets=sets
    output.innerHTML = sets.map((s,i)=>`<div class="set"><strong>Set ${i+1}:</strong> ${s.join(', ')}</div>`).join('')
  })

  exportCsv.addEventListener('click', ()=>{
    if(lastSets.length) downloadCSV(lastSets)
  })
}

main()
