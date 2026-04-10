const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');

let mainWindow;
let streamlitProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
  });

  // Wait for Streamlit to start
  setTimeout(() => {
    mainWindow.loadURL('http://localhost:8501');
  }, 5000); // increase if slow
}

app.whenReady().then(() => {
  // Start Streamlit
  streamlitProcess = spawn('python', ['-m', 'streamlit', 'run', 'app.py']);

  streamlitProcess.stdout.on('data', (data) => {
    console.log(`Streamlit: ${data}`);
  });

  streamlitProcess.stderr.on('data', (data) => {
    console.error(`Error: ${data}`);
  });

  createWindow();
});

// Close Streamlit when app closes
app.on('window-all-closed', () => {
  if (streamlitProcess) streamlitProcess.kill();
  app.quit();
});