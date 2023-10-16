// Copyright 2021 Google LLC
//
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file or at
// https://developers.google.com/open-source/licenses/bsd

const display = document.querySelector('.lineups-display');
const form = document.querySelector('.lineups');
const log = document.querySelector('.lineups-log');
const refreshButton = document.getElementById('refresh-display');
const pad = (val, len = 2) => val.toString().padStart(len, '0');

// DOM event bindings

class AlarmManager {
  constructor(display, log) {
    this.displayElement = display;
    this.logElement = log;

    this.logMessage('Manager: initializing demo');
  }

  logMessage(message) {
    console.log('logging')
    const date = new Date();
    const pad = (val, len = 2) => val.toString().padStart(len, '0');
    const h = pad(date.getHours());
    const m = pad(date.getMinutes());
    const s = pad(date.getSeconds());
    const ms = pad(date.getMilliseconds(), 3);
    const time = `${h}:${m}:${s}.${ms}`;

    const logLine = document.createElement('div');
    logLine.textContent = `[${time}] ${message}`;

    // Log events in reverse chronological order
    this.logElement.insertBefore(logLine, this.logElement.firstChild);
  }

  // Simple locking mechanism to prevent multiple concurrent refreshes from rendering duplicate
  // entries in the alarms list
  #refreshing = false;

  async refreshDisplay() {
    if (this.#refreshing) {
      return;
    } // refresh in progress, bail

    this.clearDisplay();
  }

  async clearDisplay() {
    this.displayElement.textContent = '';
  }

  async selectPlayer(playerNumber) {
    
    chrome.runtime.sendMessage('mgckfbaldncckhfiigjkipmhcffddbmh', { greeting: 'hello' },
        response => {
            console.log(response)
        }
    );

  }
}

const manager = new AlarmManager(display, log);
manager.refreshDisplay();

// Alarm display buttons

refreshButton.addEventListener('click', () => manager.refreshDisplay());

// New alarm form

form.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
  
    // Extract form values
    const type = data['type'];
    // const playerNumber = Number.parseFloat(data['player-number']);
    const playerNumber = 13
    console.log('Type: ' + type);
    // console.log('Player Number: ' + playerNumber);

    var message = `[${type.toUpperCase()}] ${playerNumber}`;
    manager.logMessage(message);
    manager.clearDisplay();
    manager.selectPlayer(playerNumber);
});
