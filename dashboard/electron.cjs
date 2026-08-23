const {app, BrowserWindow, ipcMain} = require('electron')
const path = require('path')

let mainWindow

function createWindow(){
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 750,
        minWidth: 900,
        minHeight: 600,
        frame: false,
        backgroundColor: '#080808',
        icon: path.join(__dirname, '../backend/icon.png'),
        webPreferences:{
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.cjs')
        }
    })
    mainWindow.loadURL('http://localhost:5173')
    mainWindow.on('closed', () => {mainWindow = null})
}
ipcMain.on('minimize', () => {if (mainWindow) mainWindow.minimize()})
ipcMain.on('maximize', () => {if (mainWindow) mainWindow.isMaximized() ? mainWindow.unmaximize() : mainWindow.maximize() })
ipcMain.on('close', () => {if (mainWindow) mainWindow.hide()})
app.whenReady().then(createWindow)
app.on('window-all-closed', () => app.quit())
ipcMain.on('show-window', () => {if (mainWindow) mainWindow.show() })
ipcMain.on('hide-window', () => {if (mainWindow) mainWindow.hide() })