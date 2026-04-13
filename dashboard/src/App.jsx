import {useState, useEffect} from 'react'
import axios from 'axios'

function NavButton({name, activeTab, setActiveTab, isDark}){
  return(
    <button onClick={() => setActiveTab(name)} style={{backgroundColor:activeTab == name ?(isDark?'#4ade80':'#cbbd93'):'transparent', color:activeTab === name ? '#0a1a0f' :(isDark?'#ffffff':'#0a1a0f'), border:'none', padding:'8px 16px', borderRadius:'8px', cursor:'pointer', fontSize:'14px', fontWeight:'500'}}>
      {name}
    </button>
  )
}

function NavCard({title, children, isDark}){
  return(
    <div style={{background:isDark?'#1e1d1d':'#ede8d0', border:'1px solid #8e8e8e', borderRadius:'12px', padding:'20px', marginBottom:'16px'}}>
      <p style={{fontSize:'11px', letterSpacing:'2px', color:isDark?'#6b9e7a':'#382f2e', textTransform:'uppercase', marginBottom:'12px'}}> {title} </p>
      {children}
    </div>
  )
}

function NavCardInfoRow({label, value, isDark}){
  return(
    <div style={{display:'flex', justifyContent:'space-between', padding:'8px 0', borderBottom:isDark?'1px solid #1a3a28':'1px solid #d0c8b0'}}>
      <span style={{color:isDark?'#6b9e7a':'#8a7a6a'}}>{label}</span>
      <span style={{color:isDark?'#6b9e7a':'#382f2e', fontWeight:'500'}}>{value}</span>
    </div>
  )
}

function App(){
  const[isDark , setIsDark] = useState(true)
  const[greeting, setGreeting] = useState('')
  const[activeTab, setActiveTab] = useState('Home')
  const[network, setNetwork] = useState(null)
  const[system, setSystem] = useState(null)
  const[security, setSecurity] = useState(null)
  const[apps, setApps] = useState(null)
  const[audio, setAudio] = useState(null)
  const[battery, setBattery] = useState(null)
  const[time , setTime] = useState(new Date())

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/greeting').then(response => setGreeting(response.data.message)),
    axios.get('http://127.0.0.1:8000/network').then(response => setNetwork(response.data))
    axios.get('http://127.0.0.1:8000/hardware').then(response => setSystem(response.data))
    axios.get('http://127.0.0.1:8000/security').then(response => setSecurity(response.data))
    axios.get('http://127.0.0.1:8000/apps').then(response => setApps(response.data.apps))
    axios.get('http://127.0.0.1:8000/audio').then(response => setAudio(response.data))
    axios.get('http://127.0.0.1:8000/battery').then(response => setBattery(response.data)) 
    const timeInterval = setInterval(() => setTime(new Date() , 1000))
    return () => clearInterval(timeInterval)   
  }, [])


  return (
    <div style={{background:isDark?'#000000':'#fffff0', minHeight:'100vh', color:isDark?'white':'#0a1a0f', padding:'32px', fontFamily:'sans-serif'}}>

      <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'24px'}}>
        <div>
          <h1 style={{color:isDark?'#4ade80':'#382f2e', fontSize:'32px'}}>
            Aura OS
          </h1>
          <p style={{color:isDark?'#4ade80':'#382f2e', fontSize:'14px'}}>
            Intelligent desktop companion
          </p>
        </div>

        <div style={{display:'flex'}}>
          <button onClick={() => setIsDark(!isDark)} style={{backgroundColor:'#4ade80', color:'#0a1a0f', border:'none', padding:'8px 16px', borderRadius:'8px', cursor:'pointer'}}>
            Toggle theme
          </button>
          <p style={{border:'none', padding:'8px 16px', borderRadius:'8px'}}>
            {time.toLocaleTimeString()}
          </p>
        </div>
      </div>     

      <div style={{width:'100%', background:isDark?'#1e1d1d':'#ede8d0', border:'1px solid #8e8e8e', borderRadius:'12px', padding:'20px', marginBottom:'24px'}}>
        <p style={{color:isDark?'#6b9e7a':'#382f2e', fontSize:'14px', whiteSpace:'pre-line'}}>
          {greeting}
        </p>
      </div>

      <div style={{display:'flex', marginBottom:'24px', borderBottom:'1px solid #1a3a28', gap:'8px', paddingBottom:'8px'}}>
        <nav>
          <NavButton name='Home' activeTab={activeTab} setActiveTab={setActiveTab} isDark={isDark} />
          <NavButton name='Network' activeTab={activeTab} setActiveTab={setActiveTab} isDark={isDark} />
          <NavButton name='System' activeTab={activeTab} setActiveTab={setActiveTab} isDark={isDark} />
          <NavButton name='Security' activeTab={activeTab} setActiveTab={setActiveTab} isDark={isDark} />
          <NavButton name='Apps' activeTab={activeTab} setActiveTab={setActiveTab} isDark={isDark} />
          <NavButton name='Audio' activeTab={activeTab} setActiveTab={setActiveTab} isDark={isDark} />
        </nav>
      </div>

      <div>
        {activeTab == 'Home' && 
          <NavCard title={"Home"} isDark={isDark}><p>Welcome to aura os</p></NavCard> 
        }
        {activeTab == 'Network' && 
          <NavCard title={"Network Status"} isDark={isDark}>
            <NavCardInfoRow label={'Wifi Name:'} value={network?.['Wi-Fi']?.name} isDark={isDark}/>
            <NavCardInfoRow label={"Wifi Strength:"} value={network?.['Wi-Fi']?.signal} isDark={isDark}/>
            <NavCardInfoRow label={"Wifi Speed:"} value={network?.['Wi-Fi']?.speed} isDark={isDark}/>
          </NavCard>   
        }
        {activeTab == 'System' &&
          <NavCard title={"System Information"} isDark={isDark}>
            <NavCardInfoRow label={"CPU Usage :"} value={String(system?.['CPU']?.Usage)+' %'} isDark={isDark}/>
            <NavCardInfoRow label={"CPU Cores :"} value={system?.['CPU']?.Cores} isDark={isDark}/>
            <NavCardInfoRow label={"RAM Usage :"} value={String(system?.['RAM']?.Usage)+' %'} isDark={isDark}/>
            <NavCardInfoRow label={"RAM Available :"} value={system?.['RAM']?.Available} isDark={isDark}/>
            <NavCardInfoRow label={"RAM Total :"} value={system?.['RAM']?.Total} isDark={isDark}/>
            <NavCardInfoRow label={"Disk Uage :"} value={String(system?.['Disk']?.Usage)+' %'} isDark={isDark}/>
            <NavCardInfoRow label={"Disk Available :"} value={system?.['Disk']?.Available} isDark={isDark}/>
            <NavCardInfoRow label={"Disk Total :"} value={system?.['Disk']?.Total} isDark={isDark}/>
            <NavCardInfoRow label={"GPU Name :"} value={system?.['GPU']?.[0]?.Name} isDark={isDark}/>
            <NavCardInfoRow label={"GPU VRAM :"} value={system?.['GPU']?.[0]?.VRAM} isDark={isDark}/>
            <NavCardInfoRow label={"Battery :"} value={battery?.['Percent']} isDark={isDark}/>
            <NavCardInfoRow label={"Battery Timeleft :"} value={battery?.['Time Left']} isDark={isDark}/>
            <NavCardInfoRow label={"Battery Charging :"} value={battery?.['Plugged in']?'Charging':'Not Charging'} isDark={isDark}/>
          </NavCard>
        }
        {activeTab == 'Security' &&
          <NavCard title={"Security Information"} isDark={isDark}>
            <NavCardInfoRow label={"Defender status :"} value={security?.['Defender']?.status?'On':'Off'} isDark={isDark}/>
            <NavCardInfoRow label={"Defender Real-Time Protection :"} value={security?.['Defender']?.['protection status']?'On':'Off'} isDark={isDark}/>
          </NavCard>
        }
        {activeTab == 'Apps' &&
          <NavCard title={"Running Apps"} isDark={isDark}>
            {apps?.map(app => (
              <span key = {app} style={{display:'inline-block', background:isDark?'#1a3a28':'#d0c8b0', color:isDark?'#4ade80':'#382f2e', padding:'4px 12px', borderRadius:'20px', fontSize:'13px', margin:'4px'}}>
                {app.replace('.exe','')}
              </span>
            ))} 
          </NavCard>
        }
        {activeTab == 'Audio' && 
          <NavCard title={"Audio Information"} isDark={isDark}>
            <NavCardInfoRow label={"Volume :"} value={audio?.Volume} isDark={isDark}/>
            <NavCardInfoRow label={"Mute :"} value={audio?.Mute?'Muted':'Not Muted'} isDark={isDark}/>
            <NavCardInfoRow label={"Device :"} value={audio?.Device} isDark={isDark}/>
            <NavCardInfoRow label={"Audio playing by :"} value={audio?.['Audio by']?.join(', ') || 'Nothing Playing'} isDark={isDark}/>
          </NavCard>
        }
      </div>

      
    </div>
  )
}

export default App