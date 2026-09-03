import { useState, useEffect, useRef} from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'

const DARK ={
  bg: '#080808',
  card: '#111111',
  border: '#1e1e1e',
  label: '#888888',
  value: '#f0f0f0',
  accent: '#4ade80',
  muted: '#1e1e1e',
  text: '#f0f0f0',
}
const LIGHT = {
  bg: '#f5f0e8',
  card: '#ede8dc',
  border: '#ccc5b5',
  label: '#6b6258',
  value: '#1c1917',
  accent: '#3d6b47',
  muted: '#ddd8cc',
  text: '#1c1917',
}

const API_BASE_URL = 'http://127.0.0.1:8000'

function NavButton({ name, activeTab, setActiveTab, isDark }) {
  const c = isDark ? DARK : LIGHT
  return (
    <button
      onClick={() => setActiveTab(name)}
      className={`nav-btn ${activeTab === name ? 'active' : ''}`}
      style={{
        color: activeTab === name ? c.accent : c.label,
      }}
    >
      {name}
    </button>
  )
}


function NavCard({ title, children, isDark }) {
  const c = isDark ? DARK : LIGHT
  return (
    <div
     className='card-hover'
      style={{
        background: c.card,
        border: `1px solid ${c.border}`,
        borderRadius: '12px',
        padding: '20px',
        marginBottom: '16px',
      }}
    >
      <p
        style={{
          fontSize: '11px',
          letterSpacing: '2px',
          color: c.label,
          textTransform: 'uppercase',
          marginBottom: '12px',
        }}
      >
        {title}
      </p>
      {children}
    </div>
  )
}

function NavCardInfoRow({ label, value, isDark, valueColor }) {
  const c = isDark ? DARK : LIGHT
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        padding: '8px 0',
        borderBottom: `1px solid ${c.border}`,
      }}
    >
      <span style={{ color: c.label}}>
        {label}
      </span>
      <span style={{ color: valueColor || c.value}}>
        {value}
      </span>
    </div>
  )
}

function ProgressBar({ value, color, isDark }) {
  const c = isDark ? DARK : LIGHT
  return (
    <div
      style={{
        width: '100%',
        borderRadius: '20px',
        backgroundColor: c.muted,
        height: '6px',
      }}
    >
      <div
        style={{
          borderRadius: '20px',
          backgroundColor: color,
          width: value + '%',
          height: '6px',
          transition: 'width 0.5s ease',
        }}
      />
    </div>
  )
}

function HomeRow({ label, value, isDark, valueColor, bar }) {
  const c = isDark ? DARK : LIGHT
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        padding: '8px 0',
        borderBottom: `1px solid ${c.border}`,
      }}
    >
      <span style={{ flex: '1', color: c.label}}>
        {label}
      </span>

      {bar && (
        <div style={{ flex: '2', display: 'flex', justifyContent: 'center' }}>
          <ProgressBar value={parseFloat(value)} isDark={isDark} color={valueColor} />
        </div>
      )}

      <span
        style={{
          flex: '1',
          textAlign: 'right',
          color: valueColor || c.value,
          fontWeight: '500',
          fontFamily: 'JetBrains Mono',
        }}
      >
        {value}
      </span>
    </div>
  )
}

function MessageContent({ msg, c }) {
  if (!msg.content || typeof msg.content !== 'string') return null
  if (msg.role === 'user') return <span>{msg.content}</span>

  const label = msg.type === 'weather' ? '⛅ Weather'
    : msg.type === 'code' ? '</> Code'
    : msg.type === 'data' ? '📊 Data'
    : null

  return (
    <div>
      {label && (
        <p style={{
          color: c.accent,
          fontSize: '11px',
          letterSpacing: '2px',
          textTransform: 'uppercase',
          marginBottom: '8px',
        }}>
          {label}
        </p>
      )}
      <ReactMarkdown>{msg.content}</ReactMarkdown>
    </div>
  )
}

function TitleBar({isDark}){
  const c = isDark ? DARK : LIGHT
  return(
    <div style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '8px 16px',
      background: c.bg,
      WebkitAppRegion : 'drag',
      borderBottom: `1px solid ${c.border}`
    }}>
      <span style={{
        fontFamily: 'Space Grotesk', 
        fontSize: '13px',
        color: c.label
      }}>
        VISION
      </span>
      <div style={{
        display:'flex',
        gap: '8px',
        WebkitAppRegion: 'no-drag'
      }}>
        {[
          {label: '_', action: 'minimize', hover: '#333'},
          { label: '⤢', action: 'maximize', hover: '#333' },
          { label: '✕', action: 'close',    hover: '#c0392b' },
        ].map(btn => (
          <button key={btn.action}
          onClick={() => window.electron?.[btn.action]()}
          style={{
            background: 'none', 
            border: 'none',
            color: isDark ? '#ffffff' : '#1c1917',
            cursor: 'pointer',
            width: '28px',
            height: '28px',
            borderRadius: '4px',
            fontSize: '14px'
          }}
          onMouseEnter={e => e.target.style.background = btn.hover}
          onMouseLeave={e => e.target.style.background = 'none'}
          >
            {btn.label}
          </button>
        ))}
      </div>
    </div>
  )
}

function App() {
  const [isDark, setIsDark] = useState(true)
  const [greeting, setGreeting] = useState('')
  const [activeTab, setActiveTab] = useState('Home')
  const [network, setNetwork] = useState(null)
  const [system, setSystem] = useState(null)
  const [security, setSecurity] = useState(null)
  const [apps, setApps] = useState(null)
  const [audio, setAudio] = useState(null)
  const [battery, setBattery] = useState(null)
  const [time, setTime] = useState(new Date())
  const [productivity, setProductivity] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [auraName, setAuraName] = useState(() => localStorage.getItem('auraName') || '')
  const [showNamePrompt, setShowNamePrompt] = useState(() => !localStorage.getItem('auraName'))
  const [nameInput, setNameInput] = useState('')
  const [isRecording, setIsRecording] = useState(false)
  const [transcribing, setTranscribing] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])

  const chatEndRef = useRef(null)
  const speakTimerRef = useRef(null)

  const c = isDark ? DARK : LIGHT

  const sendMessage = async (questionText = null) => {
    const question = questionText || input.trim()
    if(!question) return

    setMessages(prev => [...prev, {role: 'user', content: question}])
    setLoading(true)
    setInput('')

    try{
      const response = await fetch(API_BASE_URL+ '/ask', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question, username: auraName || 'User'}),
      })
      const data = await response.json()
      const newMsg = {role: 'vision', content: data.content, type: data.type}
      setMessages(prev => {
        const updated = [...prev, newMsg]
        axios.post(API_BASE_URL+ '/history/save', {messages: updated})
        return updated
      })
      speakResponse(data.content)
    }
    catch(error){
      console.error(error)
    }
    finally {
      setLoading(false)
    }
  }
  
  const speakResponse = (text) => {
    setIsSpeaking(true)
    axios.post(API_BASE_URL+ '/voice/speak', {question: text})
    const words = text.split(' ').length
    const ms = Math.max(3000, (words/2.17)*1000)
    speakTimerRef.current = setTimeout(() => setIsSpeaking(false), ms)
  }
  
  const handleNameSubmit = () => {
    const name = nameInput.trim() || 'Vision'
    localStorage.setItem('auraName', name)
    setAuraName(name)
    setShowNamePrompt(false)
  }

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({audio:true})
    mediaRecorderRef.current = new MediaRecorder(stream)
    audioChunksRef.current = []
    mediaRecorderRef.current.ondataavailable = e => audioChunksRef.current.push(e.data)
    mediaRecorderRef.current.start()
    setIsRecording(true)
  }

  const stopRecording = async () => {
    if(!mediaRecorderRef.current) return
    mediaRecorderRef.current.stop()
    setIsRecording(false)
    mediaRecorderRef.current.onstop = async () => {
      setTranscribing(true)
      try{
        const blob = new Blob(audioChunksRef.current, {type: 'audio/wav'})
        const formData = new FormData()
        formData.append('audio', blob, 'recording.wav')
        const res = await axios.post(API_BASE_URL+ '/voice/input', formData)
        const transcript = res.data.transcript
        if (transcript){
          setInput(transcript)
          sendMessage(transcript)
        }
      }
      finally{
        setTranscribing(false)
      }
    }
  }

  useEffect(() => {
    axios.get(API_BASE_URL+ '/history')
      .then(res => {if (res.data.messages?.length) setMessages(res.data.messages)})

    axios.get(API_BASE_URL+ '/greeting')
      .then(response => setGreeting(response.data.message))

    const fetchInstant = async () => {
      try{
        const r1 = await axios.get(API_BASE_URL+ '/audio')
        setAudio(r1.data)
      }catch (error){
        console.error('Error Fetching Instant data:', error)
      }
    }

    const fetchFastData = async () => {
      try {
        const r1 = await axios.get(API_BASE_URL+ '/hardware')
        setSystem(r1.data)
        const r2 = await axios.get(API_BASE_URL+ '/battery')
        setBattery(r2.data)
      } catch (error) {
        console.error('Error fetching fast data:', error)
      }
    }

    const fetchSlowData = async () => {
      try {
        const r1 = await axios.get(API_BASE_URL+ '/network')
        setNetwork(r1.data)
        const r2 = await axios.get(API_BASE_URL+ '/security')
        setSecurity(r2.data)
        const r3 = await axios.get(API_BASE_URL+ '/apps')
        setApps(r3.data.apps)
        const r4 = await axios.get(API_BASE_URL+ '/productivity')
        setProductivity(r4.data)
        const r5 = await axios.get(API_BASE_URL+ '/predictions')
        setPrediction(r5.data)
      } catch (error) {
        console.error('Error fetching slow data:', error)
      }
    }

    fetchFastData()
    fetchSlowData()
    fetchInstant()

    const Instant = setInterval(fetchInstant, 500)
    const fastInterval = setInterval(fetchFastData, 2000)
    const slowInterval = setInterval(fetchSlowData, 30000)
    const timeInterval = setInterval(() => setTime(new Date()), 1000)

    return () => {
      clearInterval(Instant)
      clearInterval(fastInterval)
      clearInterval(slowInterval)
      clearInterval(timeInterval)
    }
  }, [])

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth'})
  }, [messages, loading])


  return (
    <div
      style={{
        background: c.bg,
        height: '100vh',
        overflow: 'hidden',
        color: c.text,
        fontFamily: "'Space Grotesk', sans-serif",
        animation: 'fadeIn 0.4s ease',
        '--accent': c.accent,
        display: 'flex',
        flexDirection: 'column'
      }}
    >
      <TitleBar isDark={isDark}/>
      <div style={{ padding: '32px', flex: 1, overflowY: 'auto' }}>

      {showNamePrompt && (
        <div style={{
          position: 'fixed', 
          inset: 0,
          background: 'rgba(0,0,0,0.85)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 999,
        }}>
          <div style={{
            background: c.card,
            border: `1px solid ${c.border}`,
            borderRadius: '16px',
            padding: '40px',
            width: '360px',
            display: 'flex',
            flexDirection: 'column',
            gap: '16px',
            textAlign: 'center',
          }}>
            <p style={{
              color: c.accent,
              fontSize: '11px',
              letterSpacing: '2px', 
              textTransform: 'uppercase',
            }}>
              Welcome
            </p>
            <h2 style={{
              color: c.text,
              fontSize: '22px',
              fontWeight: '700',
              margin: '0'
            }}>
              What should I call you?
            </h2>
            <p style={{
              color: c.label,
              fontSize: '13px',
              margin: '0',
            }}>
              I'll use this to personalize your experience.
            </p>
            <input type="text" 
            value={nameInput} 
            onChange={e => setNameInput(e.target.value)} 
            onKeyDown={e => {if (e.key === 'Enter') handleNameSubmit()}} 
            placeholder='Your Name...' 
            autoFocus
            style={{
              background: c.bg,
              border: `1px solid ${c.border}`,
              borderRadius: '8px',
              padding: '10px 14px',
              fontSize: '14px',
              color: c.accent,
              outline: 'none',
              fontFamily: "'Space Grotesk', sans-serif",
              textAlign: 'center',
            }}/>
            <button onClick={handleNameSubmit}
            style={{
              backgroundColor: c.accent,
              color: c.bg,
              border: 'none',
              borderRadius: '8px',
              padding: '10px',
              fontSize: '14px',
              fontWeight: '600',
              cursor: 'pointer',
              fontFamily: "'Space Grotesk', sans-serif",
            }}>
              Let's go -{'>'}
            </button>
          </div>

        </div>
      )}

      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '24px',
        }}
      >
        <div>
          <h1 style={{ color: c.accent, fontSize: '40px', fontWeight: '700' }}>
            <span style={{
              display: 'inline-block',
              width: '10px',
              height: '10px',
              borderRadius: '50%',
              backgroundColor: c.accent,
              marginRight: '12px',
            }} /> {auraName ? `${auraName}'s` : 'Vision'} — AI Assistant
          </h1>
          <p style={{ color: c.label, fontSize: '14px' }}>
            Vision — Intelligent desktop companion
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <button
            onClick={() => setIsDark(!isDark)}
            style={{
              backgroundColor: c.muted,
              color: c.bg,
              border: 'none',
              padding: '8px 16px',
              borderRadius: '8px',
              cursor: 'pointer',
            }}
          >
            {isDark ? '☀️' : '🌙'}
          </button>
          <p style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: '14px', padding: '8px 16px' }}>
            {time.toLocaleTimeString()}
          </p>
        </div>
      </div>

      <div
        style={{
          width: '100%',
          background: c.card,
          border: `1px solid ${c.border}`,
          borderRadius: '12px',
          padding: '20px',
          marginBottom: '24px',
        }}
      >
        <p style={{ color: c.accent, fontSize: '14px', whiteSpace: 'pre-line' }}>
          {greeting}
        </p>
      </div>

      <div
        style={{
          display: 'flex',
          marginBottom: '24px',
          borderBottom: `1px solid ${c.border}`,
          gap: '8px',
          paddingBottom: '8px',
        }}
      >
        <nav>
          {['Home', 'Network', 'System', 'Security', 'Apps', 'Audio', 'Vision'].map(tab => (
            <NavButton
              key={tab}
              name={tab}
              activeTab={activeTab}
              setActiveTab={setActiveTab}
              isDark={isDark}
            />
          ))}
        </nav>
      </div>

      <div>
        {activeTab === 'Home' && (
          <div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>

              <NavCard title="Quick Stat" isDark={isDark}>
                <HomeRow
                  label="Battery"
                  value={String(battery?.['Percent']) + ' %'}
                  isDark={isDark}
                  bar
                  valueColor={battery?.Percent > 50 ? '#4ade80' : battery?.Percent > 20 ? '#fb923c' : '#ef4444'}
                />
                <HomeRow label="Wi-Fi" value={network?.['Wi-Fi']?.name} isDark={isDark} />
              </NavCard>

              <NavCard title="System Health" isDark={isDark}>
                <HomeRow
                  label="CPU"
                  value={String(system?.['CPU']?.Usage) + ' %'}
                  isDark={isDark}
                  bar
                  valueColor={isDark ? '#4ade80' : '#382f2e'}
                />
                <HomeRow
                  label="RAM"
                  value={String(system?.['RAM']?.Usage) + ' %'}
                  isDark={isDark}
                  bar
                  valueColor={isDark ? '#60a5fa' : '#800000'}
                />
              </NavCard>

              <NavCard title="Active Apps" isDark={isDark}>
                {apps?.map(app => (
                  <span
                    key={app}
                    className='tag'
                    style={{background: c.muted, color: c.accent}}
                  >
                    {app.replace('.exe', '')}
                  </span>
                ))}
              </NavCard>

              <NavCard title="Security Status" isDark={isDark}>
                <HomeRow
                  label="Defender"
                  value={security?.['Defender']?.['protection status'] ? 'On' : 'Off'}
                  isDark={isDark}
                  valueColor={security?.['Defender']?.status ? '#4ade80' : '#ef4444'}
                />
              </NavCard>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>

              <NavCard title="Productivity Report" isDark={isDark}>
                <HomeRow label="Total Sessions" value={productivity?.['total_session']} isDark={isDark} />
                <HomeRow
                  label="Avg Duration"
                  value={productivity?.['avg_duration'] ? (productivity['avg_duration'] / 60).toFixed(1) + ' hrs' : '—'}
                  isDark={isDark}
                />
                <HomeRow label="Productive Day" value={productivity?.['most_productive_day']} isDark={isDark} />
                <HomeRow
                  label="Peak Hours"
                  value={productivity?.['peak_hours']?.map(h => h[0] + ':00').join(', ')}
                  isDark={isDark}
                />
              </NavCard>

              <NavCard title="Prediction" isDark={isDark}>
                <HomeRow label="Battery Drain" value={String(prediction?.['battery_drain']) + ' %'} isDark={isDark} />
                <HomeRow label="Next App" value={prediction?.['next_app']} isDark={isDark} />
                <HomeRow label="Session End Time" value={String(prediction?.['session_end']) + ':00'} isDark={isDark} />
              </NavCard>

            </div>
          </div>
        )}

        {activeTab === 'Network' && (
          <NavCard title="Network Status" isDark={isDark}>
            <NavCardInfoRow label="Wifi Name" value={network?.['Wi-Fi']?.name} isDark={isDark} />
            <NavCardInfoRow label="Wifi Strength" value={network?.['Wi-Fi']?.signal} isDark={isDark} />
            <ProgressBar
              value={parseInt(network?.['Wi-Fi']?.signal)}
              color={
                parseInt(network?.['Wi-Fi']?.signal) > 70 ? '#4ade80' :
                parseInt(network?.['Wi-Fi']?.signal) > 30 ? '#fb923c' : '#ef4444'
              }
              isDark={isDark}
            />
            <NavCardInfoRow label="Wifi Speed" value={network?.['Wi-Fi']?.speed} isDark={isDark} />
          </NavCard>
        )}

        {activeTab === 'System' && (
          <NavCard title="System Information" isDark={isDark}>
            <NavCardInfoRow label="CPU Usage" value={String(system?.['CPU']?.Usage) + ' %'} isDark={isDark} />
            <ProgressBar value={system?.['CPU']?.Usage} color={isDark ? '#4ade80' : '#382f2e'} isDark={isDark} />
            <NavCardInfoRow label="CPU Cores" value={system?.['CPU']?.Cores} isDark={isDark} />
            <NavCardInfoRow label="RAM Usage" value={String(system?.['RAM']?.Usage) + ' %'} isDark={isDark} />
            <ProgressBar value={system?.['RAM']?.Usage} color={isDark ? '#60a5fa' : '#800000'} isDark={isDark} />
            <NavCardInfoRow label="RAM Available" value={system?.['RAM']?.Available} isDark={isDark} />
            <NavCardInfoRow label="RAM Total" value={system?.['RAM']?.Total} isDark={isDark} />
            <NavCardInfoRow label="Disk Usage" value={String(system?.['Disk']?.Usage) + ' %'} isDark={isDark} />
            <ProgressBar value={system?.['Disk']?.Usage} color={isDark ? '#fb923c' : '#556b2f'} isDark={isDark} />
            <NavCardInfoRow label="Disk Available" value={system?.['Disk']?.Available} isDark={isDark} />
            <NavCardInfoRow label="Disk Total" value={system?.['Disk']?.Total} isDark={isDark} />
            <NavCardInfoRow label="GPU Name" value={system?.['GPU']?.[0]?.Name} isDark={isDark} />
            <NavCardInfoRow label="GPU VRAM" value={system?.['GPU']?.[0]?.VRAM} isDark={isDark} />
            <NavCardInfoRow label="Battery" value={battery?.['Percent'] + ' %'} isDark={isDark} />
            <ProgressBar
              value={battery?.Percent}
              color={battery?.Percent > 50 ? '#4ade80' : battery?.Percent > 20 ? '#fb923c' : '#ef4444'}
              isDark={isDark}
            />
            <NavCardInfoRow label="Battery Time Left" value={battery?.['Time Left']} isDark={isDark} />
            <NavCardInfoRow
              label="Battery Charging"
              value={battery?.['Plugged in'] ? 'Charging' : 'Not Charging'}
              isDark={isDark}
            />
          </NavCard>
        )}

        {activeTab === 'Security' && (
          <NavCard title="Security Information" isDark={isDark}>
            <p style={{ color: c.accent, fontWeight: 'bold', padding: '4px 0' }}>
              Defender
            </p>
            <NavCardInfoRow
              label="Status"
              value={security?.['Defender']?.status ? 'On' : 'Off'}
              isDark={isDark}
              valueColor={security?.['Defender']?.status ? '#6b9e80' : '#ef4444'}
            />
            <NavCardInfoRow
              label="Real-Time Protection"
              value={security?.['Defender']?.['protection status'] ? 'On' : 'Off'}
              isDark={isDark}
              valueColor={security?.['Defender']?.['protection status'] ? '#6b9e80' : '#ef4444'}
            />
            <NavCardInfoRow
              label="Reboot Required"
              value={security?.['Defender']?.['reboot required'] ? 'Yes' : 'No'}
              isDark={isDark}
            />
            <NavCardInfoRow
              label="Last Scan"
              value={security?.['Defender']?.['last quick scan time']}
              isDark={isDark}
            />
            <p style={{ color: c.accent, fontWeight: 'bold', padding: '4px 0', marginTop: '10px' }}>
              Firewall
            </p>
            <NavCardInfoRow
              label="Domain"
              value={security?.['Firewall']?.Domain}
              isDark={isDark}
              valueColor={security?.['Firewall']?.Domain ? '#6b9e80' : '#ef4444'}
            />
            <NavCardInfoRow
              label="Public"
              value={security?.['Firewall']?.Public}
              isDark={isDark}
              valueColor={security?.['Firewall']?.Public ? '#6b9e80' : '#ef4444'}
            />
            <NavCardInfoRow
              label="Private"
              value={security?.['Firewall']?.Private}
              isDark={isDark}
              valueColor={security?.['Firewall']?.Private ? '#6b9e80' : '#ef4444'}
            />
          </NavCard>
        )}

        {activeTab === 'Apps' && (
          <NavCard title="Running Apps" isDark={isDark}>
            {apps?.map(app => (
              <span
                key={app}
                className='tag'
                style={{background: c.muted, color: c.accent}}
              >
                {app.replace('.exe', '')}
              </span>
            ))}
          </NavCard>
        )}

        {activeTab === 'Audio' && (
          <NavCard title="Audio Information" isDark={isDark}>
            <NavCardInfoRow label="Volume" value={audio?.Volume + ' %'} isDark={isDark} />
            <ProgressBar
              value={audio?.Volume}
              color={audio?.Volume > 70 ? '#ef4444' : audio?.Volume > 30 ? '#4ade80' : 'grey'}
              isDark={isDark}
            />
            <NavCardInfoRow label="Mute" value={audio?.Mute ? 'Muted' : 'Not Muted'} isDark={isDark} />
            <NavCardInfoRow label="Device" value={audio?.Device} isDark={isDark} />
            <NavCardInfoRow
              label="Audio Playing By"
              value={audio?.['Audio by']?.join(', ') || 'Nothing Playing'}
              isDark={isDark}
            />
          </NavCard>
        )}

        {activeTab === 'Vision' && (
          <div
            style={{
              height: '60vh',
              display: 'flex',
              flexDirection: 'column',
              background: c.card,
              border: `1px solid ${c.border}`,
              borderRadius: '12px',
              overflow: 'hidden',
            }}
          >
            <div
              style={{
                padding: '12px 20px',
                borderBottom: `1px solid ${c.border}`,
              }}
            >
              <p
                style={{
                  fontSize: '11px',
                  letterSpacing: '2px',
                  color: c.accent,
                  textTransform: 'uppercase',
                  margin: 0,
                }}
              >
                {auraName ? `${auraName}'s - Assistant` : 'Vision - AI Assistant'}
              </p>
            </div>

            <div
              className='chat-messages'
              style={{
                flex: 1,
                overflowY: 'auto',
                padding: '16px',
                display: 'flex',
                flexDirection: 'column',
                gap: '12px',
              }}
            >
              {messages.length === 0 && (
                <p
                  style={{
                    color: c.label,
                    fontSize: '13px',
                    textAlign: 'center',
                    marginTop: '40px',
                  }}
                >
                  Ask Vision anything about your system or anything else...
                </p>
              )}

              {messages.map((msg, index) => (
                <div
                  key={index}
                  style={{
                    display: 'flex',
                    justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                  }}
                >
                  <div
                    style={{
                      padding: '10px 14px',
                      borderRadius: '10px',
                      maxWidth: '75%',
                      backgroundColor: msg.role === 'user' ? c.muted : c.bg,
                      color: c.text,
                      wordBreak: 'break-word',
                      fontSize: '14px',
                      lineHeight: '1.5',
                      border: msg.role === 'user' ? 'none' : `1px solid ${c.border}`,
                    }}
                  >
                    <MessageContent msg={msg} c={c} />
                  </div>
                </div>
              ))}

              {loading && (
                <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
                  <div
                    style={{
                      display: 'flex',
                      gap: '4px',
                      alignItems: 'center',
                    }}
                  >
                    <span className='typing-dot' style={{backgroundColor: c.accent}} />
                    <span className='typing-dot' style={{backgroundColor: c.accent}} />
                    <span className='typing-dot' style={{backgroundColor: c.accent}} />
                  </div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>

            <div
              style={{
                borderTop: `1px solid ${c.border}`,
                padding: '12px 16px',
                display: 'flex',
                gap: '8px',
              }}
            >
              <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => { if (e.key === 'Enter') sendMessage() }}
                placeholder="Ask Vision..."
                style={{
                  flex: 1,
                  background: c.bg,
                  border: `1px solid ${c.border}`,
                  borderRadius: '8px',
                  padding: '8px 14px',
                  outline: 'none',
                  fontSize: '14px',
                  color: c.text,
                  fontFamily: "'Space Grotesk', sans-serif",
                }}
              />
              <button
                onClick={sendMessage}
                style={{
                  backgroundColor: c.accent,
                  color: c.bg,
                  padding: '8px 20px',
                  borderRadius: '8px',
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '600',
                  fontFamily: "'Space Grotesk', sans-serif",
                }}
              >
                Send
              </button>
              <button
                onMouseDown={startRecording}
                onMouseUp={stopRecording}
                style={{
                  backgroundColor: isRecording ? '#ef4444' : transcribing ? '#fb923c' : c.muted,
                  color: c.accent,
                  padding: '8px 14px',
                  borderRadius: '8px',
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: '18px',
                }}
              >
                {transcribing ? '⏳' : '🎙️'}
              </button>
              {
                isSpeaking && (
                  <button
                    onClick={() => {
                      axios.post(API_BASE_URL+ '/voice/stop')
                      clearTimeout(speakTimerRef.current)
                      setIsSpeaking(false)
                    }}
                    style={{
                      backgroundColor: '#ef4444',
                      color: '#fff',
                      padding: '8px 14px',
                      borderRadius: '8px',
                      border: 'none',
                      cursor: 'pointer',
                      fontSize: '14px',
                      fontWeight: '600'
                    }}
                  >
                    ⏹ Stop
                  </button>
                )
              }
            </div>
          </div>
        )}

      </div>
      </div>
    </div>
  )
}

export default App
