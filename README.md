# AuraOS 

An AI-native desktop layer that learns you.

AuraOS watches how you work, understands your patterns, 
and guides you every time you log in — like JARVIS for your computer.

## Current Features
- ✅ Process tracker and app filter
- ✅ Essential Windows services monitor
- ✅ Network Status (WiFi , Bluetooth , Ethernet)
- ✅ Security Status (Defender + Firewall)
- ✅ Audio Status (Volume , Mute , Device , Audio Source)
- ✅ Power Status (Battery Percentage , Charging)
- ✅ Hardware monitoring (CPU , RAM , DISK , GPU)
- ✅ SQLite memory database
- ✅ Pattern learning engine
- ✅ Morning greeting with insights
- ✅ Smart notifications

## Tech Stack
- Python
- psutil , WMI , pywifi , pycaw , plyer
- subprocess
- SQLite
- FastAPI
- React

# Roadmap
## Phase 1 - Foundation 
- [x] activity_tracker.py   →  monitors all system activity
- [x] aura_memory.py        →  SQLite database memory
- [x] pattern_engine.py     →  learns your usage patterns
- [x] greeting.py           →  personalized morning greeting
- [x] notifications.py      →  smart system alerts
- [x] main.py               →  brings everything alive
- [x] api.py                →  FastAPI backend

## Phase 2 - Dashboard
- [x] React dashboard
- [x] Dark/light theme
- [x] Typography (Space Grotesk + JetBrains Mono fonts)
- [x] Progress bars (CPU, RAM, Disk, Battery, WiFi)
- [x] Color coded status indicators
- [x] Live updating (2s fast, 30s slow)
- [x] Home tab overview grid
- [x] Background notifications thread
- [x] All 6 tabs working
⬜ Polish and animation

## Phase 3 - Intelligence
⬜ Better pattern analysis
     - peak productivity hours
     - most used apps by time of day
     - battery drain patterns
     - network usage patterns

⬜ Productivity insights
     - daily session reports
     - weekly usage summary
     - "You were most productive on Tuesday"

⬜ Anomaly detection
     - unusual login times
     - "You don't usually turn on at 3am — everything ok?"
     - unusual app usage
     - sudden CPU/RAM spikes

⬜ Smarter greeting
     - personalized based on patterns
     - weather integration
     - calendar awareness (if connected)

⬜ Usage predictions
     - "Based on your pattern, you'll need to charge in 2 hours"
     - "You usually open VS Code around this time"

## Built by
Shourya Verma 
Started 4th semester 
Started from Zero. Building something real.

## The WHY?
I want something that help us in out day to day life , i got the idea to build Aura-OS from a memory of my childhood .
Like how my mother helps me in everything , similary I want someone to help me everytime when I do my work on my system .
So from there I got thought about Aura-OS

## Vision
A desktop OS layer that knows you better than yesterday , learn from today and get better for tomorrow.