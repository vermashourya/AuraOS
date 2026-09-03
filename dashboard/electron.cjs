const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const { spawn } = require('child_process')

let mainWindow
let backendProcess

function startBackend() {
    const isDev = !app.isPackaged
    if (isDev) return  // dev: backend started manually

    const backendExe = path.join(process.resourcesPath, 'backend', 'auraos_backend.exe')
    backendProcess = spawn(backendExe, [], { detached: false })
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 750,
        minWidth: 900,
        minHeight: 600,
        frame: false,
        backgroundColor: '#080808',
        icon: path.join(__dirname, '../backend/icon.png'),
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.cjs')
        }
    })

    const isDev = !app.isPackaged
    if (isDev) {
        mainWindow.loadURL('http://localhost:5173')
    } else {
        mainWindow.loadFile(path.join(__dirname, 'dist', 'index.html'))
    }

    mainWindow.on('closed', () => { mainWindow = null })
}

ipcMain.on('minimize', () => { if (mainWindow) mainWindow.minimize() })
ipcMain.on('maximize', () => { if (mainWindow) mainWindow.isMaximized() ? mainWindow.unmaximize() : mainWindow.maximize() })
ipcMain.on('close', () => { if (mainWindow) mainWindow.hide() })
ipcMain.on('show-window', () => { if (mainWindow) mainWindow.show() })
ipcMain.on('hide-window', () => { if (mainWindow) mainWindow.hide() })

app.whenReady().then(() => {
    startBackend()
    // small delay so backend has time to start before UI loads
    setTimeout(createWindow, app.isPackaged ? 3000 : 0)
})

app.on('window-all-closed', () => {
    if (backendProcess) backendProcess.kill()
    app.quit()
})
