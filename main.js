const { app, BrowserWindow, globalShortcut } = require('electron')
let mainWindow;

process.env.ELECTRON_ENABLE_SECURITY_WARNINGS = false;
process.env.ELECTRON_DISABLE_SECURITY_WARNINGS = true;


app.whenReady().then( function(){

	mainWindow = new BrowserWindow({
		width:800, 
		height:800, 
		resizable:false,
		
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true,
        }

	});

	mainWindow.removeMenu();
	mainWindow.webContents.openDevTools();
	mainWindow.loadFile('index.html');
	
	app.on('window-all-closed', () => app.quit());

});
