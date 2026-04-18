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

function NavCardInfoRow({label, value, isDark, valueColor}){
  return(
    <div style={{display:'flex', justifyContent:'space-between', padding:'8px 0', borderBottom:isDark?'1px solid #1a3a28':'1px solid #d0c8b0'}}>
      <span style={{color:isDark?'#6b9e7a':'#8a7a6a'}}>{label}</span>
      <span style={{color: valueColor || (isDark?'#6b9e7a':'#382f2e'), fontWeight:'500'}}>{value}</span>
    </div>
  )
}

function ProgressBar({value, color, isDark}){
  return(
    <div style={{width:'100%', borderRadius:'20px', backgroundColor:isDark?'#2a2a2a':'#fffff0', height:'6px'}}>
      <div style={{borderRadius:'20px', backgroundColor:color, width:value +'%', height:'6px'}}></div>
    </div>
  )
}

function Home({label, value, isDark, valueColor, bar}){
  return(
    <div style={{display:'flex', alignItems:'center', padding:'8px 0', borderBottom:isDark?'1px solid #1a3a28':'1px solid #d0c8b0'}}>
      <span style={{flex:'1', color:isDark?'#6b9e7a':'#8a7a6a'}}> {label} </span>
      {bar && (
        <div style={{flex:'2', display:'flex', justifyContent:'center'}}>
          <ProgressBar value={value} isDark={isDark} color={valueColor}/>
        </div>
      )}
      <span style={{flex:'1', textAlign:'right', color:valueColor || (isDark?'#6b9e80':'#382f2e'), fontWeight:'500', fontFamily:'JetBrains Mono'}}>{value}</span>
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
    axios.get('http://127.0.0.1:8000/greeting').then(response => setGreeting(response.data.message)) 

    const fetchFastData = async() =>{
      try{
        const r1 = await axios.get('http://127.0.0.1:8000/hardware'); 
        setSystem(r1.data);
        const r2 = await axios.get('http://127.0.0.1:8000/battery'); 
        setBattery(r2.data);
        const r3 = await axios.get('http://127.0.0.1:8000/audio');
        setAudio(r3.data);
      }
      catch (error){
        console.error('Error fetching data:', error);
      }
    };
    fetchFastData()
    const fastData = setInterval(fetchFastData, 2000);

    const fetchSlowData = async() =>{
      try{
        const r1 = await axios.get('http://127.0.0.1:8000/network');
        setNetwork(r1.data);
        const r2 = await axios.get('http://127.0.0.1:8000/security');
        setSecurity(r2.data);
        const r3 = await axios.get('http://127.0.0.1:8000/apps');
        setApps(r3.data.apps);
      }
      catch (error){
        console.error('Error Fetching data:', error);
      }
    }
    fetchSlowData()
    const slowData = setInterval(fetchSlowData, 30000)

    const timeInterval = setInterval(() => setTime(new Date()) , 1000)
    return () => {
      clearInterval(timeInterval) 
      clearInterval(fastData)
      clearInterval(slowData)
    }
  }, [])

  return (
    <div style={{background:isDark?'#000000':'#fffff0', minHeight:'100vh', color:isDark?'white':'#0a1a0f', padding:'32px', fontFamily:"'Space Grotesk', sans-serif"}}>

      <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'24px'}}>
        <div>
          <h1 style={{color:isDark?'#4ade80':'#382f2e', fontSize:'40px', fontWeight:'700', letterSpacing:'-1'}}>
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
          <p style={{border:'none', padding:'8px 16px', borderRadius:'8px', fontFamily:"'JetBrains Mono', monospace", fontSize:'14px'}}>
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
          <div>
            <div style={{display:'grid', gridTemplateColumns:'repeat(4,1fr)', gap:'16px'}}>
              <div>
                <NavCard title={'Quick Stat'} isDark={isDark}>
                  <Home label={'Battery'} value={String(battery?.['Percent'])+' %'} isDark={isDark} bar={true} valueColor={battery?.Percent > 50 ?'#4ade80':battery?.Percent >20?'#fb923c':'#ef4444'}/>
                  <Home label={'Wi-Fi'} value={network?.['Wi-Fi']?.name} isDark={isDark}/>
                </NavCard>
              </div>
              <div>
                <NavCard title={'System Health'} isDark={isDark}>
                  <Home label={'CPU'} value={String(system?.['CPU']?.Usage)+' %'} isDark={isDark} bar={true} valueColor={isDark?'#4ade80':'#382f2e'}/> 
                  <Home label={'RAM'} value={String(system?.['RAM']?.Usage)+' %'} isDark={isDark} bar={true} valueColor={isDark?'#60a5fa':'#800000'}/>
                </NavCard>
              </div>
              <div>
                <NavCard title={'Active Apps'} isDark={isDark}>
                  {apps?.map(app => (
                    <span key={app} style={{display:'inline-block', background:isDark?'#1a3a28':'#d0c8b0', color:isDark?'#4ade80':'#382f2e', padding:'4px 12px', borderRadius:'20px', fontSize:'13px', margin:'4px'}} >
                      {app.replace('.exe','')}
                    </span>
                  ))}
                </NavCard>
              </div>
              <div>
                <NavCard title={'Security Status'} isDark={isDark}>
                  <Home label={'Defender'} value={security?.['Defender']?.['protection status']?'On':'Off'} isDark={isDark} valueColor={security?.['Defender']?.status ? '#4ade80':'#ef4444'}/>
                  {/* <Home label={'FireWall'} value={security?.['Firewall']} isDark={isDark}/> */}
                </NavCard>
              </div>
            </div>
          </div>
        }
        {activeTab == 'Network' && 
          <NavCard title={"Network Status"} isDark={isDark}>
            <NavCardInfoRow label={'Wifi Name'} value={network?.['Wi-Fi']?.name} isDark={isDark}/>
            <NavCardInfoRow label={"Wifi Strength"} value={network?.['Wi-Fi']?.signal} isDark={isDark}/>
            <ProgressBar value={parseInt(network?.['Wi-Fi']?.signal)} color={parseInt(network?.['Wi-Fi']?.signal) > 70 ?'#4ade80':parseInt(network?.['Wi-Fi']?.signal) > 30 ?'#fb923c':'#ef4444'} isDark={isDark}/>
            <NavCardInfoRow label={"Wifi Speed"} value={network?.['Wi-Fi']?.speed} isDark={isDark}/>
          </NavCard>   
        }
        {activeTab == 'System' &&
          <NavCard title={"System Information"} isDark={isDark}>
            <NavCardInfoRow label={"CPU Usage "} value={String(system?.['CPU']?.Usage)+' %'} isDark={isDark}/>
            <ProgressBar value={system?.['CPU']?.Usage} color={isDark?'#4ade80':'#382f2e'} isDark={isDark}/>
            <NavCardInfoRow label={"CPU Cores"} value={system?.['CPU']?.Cores} isDark={isDark}/>
            <NavCardInfoRow label={"RAM Usage"} value={String(system?.['RAM']?.Usage)+' %'} isDark={isDark}/>
            <ProgressBar value={system?.['RAM']?.Usage} color={isDark?'#60a5fa':'#800000'} isDark={isDark}/>
            <NavCardInfoRow label={"RAM Available"} value={system?.['RAM']?.Available} isDark={isDark}/>
            <NavCardInfoRow label={"RAM Total"} value={system?.['RAM']?.Total} isDark={isDark}/>
            <NavCardInfoRow label={"Disk Usage"} value={String(system?.['Disk']?.Usage)+' %'} isDark={isDark}/>
            <ProgressBar value={system?.['Disk']?.Usage} color={isDark?'#fb923c':'#556b2f'} isDark={isDark}/>
            <NavCardInfoRow label={"Disk Available"} value={system?.['Disk']?.Available} isDark={isDark}/>
            <NavCardInfoRow label={"Disk Total"} value={system?.['Disk']?.Total} isDark={isDark}/>
            <NavCardInfoRow label={"GPU Name"} value={system?.['GPU']?.[0]?.Name} isDark={isDark}/>
            <NavCardInfoRow label={"GPU VRAM"} value={system?.['GPU']?.[0]?.VRAM} isDark={isDark}/>
            <NavCardInfoRow label={"Battery"} value={battery?.['Percent']} isDark={isDark}/>
            <ProgressBar value={battery?.Percent} color={battery?.Percent > 50 ?'#4ade80':battery?.Percent >20?'#fb923c':'#ef4444'} isDark={isDark}/>
            <NavCardInfoRow label={"Battery Timeleft"} value={(battery?.['Time Left'])} isDark={isDark}/>
            <NavCardInfoRow label={"Battery Charging"} value={battery?.['Plugged in']?'Charging':'Not Charging'} isDark={isDark}/>
          </NavCard>
        }
        {activeTab == 'Security' &&
          <NavCard title={"Security Information"} isDark={isDark}> 
            <p style={{color:isDark?'#4ade80':'#382f2e', fontWeight:'bold', padding:'4px 0'}}>Defender</p>
            <NavCardInfoRow label={"Status"} value={security?.['Defender']?.status?'On':'Off'} isDark={isDark} valueColor={security?.['Defender']?.status ? '#6b9e80':'#ef4444'}/>
            <NavCardInfoRow label={"Real-Time Protection"} value={security?.['Defender']?.['protection status']?'On':'Off'} isDark={isDark} valueColor={security?.['Defender']?.['protection status'] ? '#6b9e80':'#ef4444'}/>
            <NavCardInfoRow label={"Reboot Required"} value={security?.['Defender']?.['reboot required']?'Yes':'No'} isDark={isDark} />
            <NavCardInfoRow label={"Last Scan"} value={security?.['Defender']?.['last quick scan time']} isDark={isDark}/>
            <p style={{color:isDark?'#4ade80':'#382f2e', fontWeight:'bold', padding:'4px 0', marginTop:'10px'}}>Firewall</p>
            <NavCardInfoRow label={"Domain"} value={security?.['Firewall']?.Domain} isDark={isDark} valueColor={security?.['Firewall']?.Domain ? '#6b9e80':'#ef4444'}/>
            <NavCardInfoRow label={"Public"} value={security?.['Firewall']?.Public} isDark={isDark} valueColor={security?.['Firewall']?.Public ? '#6b9e80':'#ef4444'}/>
            <NavCardInfoRow label={"Private"} value={security?.['Firewall']?.Private} isDark={isDark} valueColor={security?.['Firewall']?.Private ? '#6b9e80':'#ef4444'}/>
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
            <NavCardInfoRow label={"Volume"} value={audio?.Volume} isDark={isDark}/>
            <ProgressBar value={audio?.Volume} color={audio?.Volume > 70 ?'#ef4444':audio?.Volume > 30?'#4ade80':'grey'} isDark={isDark}/>
            <NavCardInfoRow label={"Mute"} value={audio?.Mute?'Muted':'Not Muted'} isDark={isDark}/>
            <NavCardInfoRow label={"Device"} value={audio?.Device} isDark={isDark}/>
            <NavCardInfoRow label={"Audio playing by"} value={audio?.['Audio by']?.join(', ') || 'Nothing Playing'} isDark={isDark}/>
          </NavCard>
        }
      </div>
      
    </div>
  )
}

export default App