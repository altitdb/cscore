 const display = document.querySelector('.lineups-display')
 const form = document.querySelector('.lineups')
 const log = document.querySelector('.lineups-log')
 const refreshButton = document.getElementById('refresh-display')
 const pad = (val, len = 2) => val.toString().padStart(len, '0')

 class AlarmManager {

   constructor(display, log) {
     this.displayElement = display,
     this.logElement = log,
     this.logMessage('Manager: initializing demo')
   }

   logMessage(message) {
     console.log('logging')
     const date = new Date()
     const pad = (val, len = 2) => val.toString().padStart(len, '0')
     const h = pad(date.getHours())
     const m = pad(date.getMinutes())
     const s = pad(date.getSeconds())
     const ms = pad(date.getMilliseconds(), 3)
     const time = `${h}:${m}:${s}.${ms}`

     const logLine = document.createElement('div')
     logLine.textContent = `[${time}] ${message}`

     this.logElement.insertBefore(logLine, this.logElement.firstChild)
   }

   #refreshing = false

   async refreshDisplay() {
     if (this.#refreshing) {
       return
     }

     this.clearDisplay()
   }

   async clearDisplay() {
     this.displayElement.textContent = ''
   }

   async selectPlayer(playerNumber) {
    
     chrome.runtime.sendMessage('mgckfbaldncckhfiigjkipmhcffddbmh', { greeting: 'hello' },
         response => {
             console.log(response)
         }
     )

   }
 }

 const manager = new AlarmManager(display, log)
 manager.refreshDisplay()

 refreshButton.addEventListener('click', () => manager.refreshDisplay())

 form.addEventListener('submit', (event) => {
     event.preventDefault()
     // const formData = new FormData(form)
     // const data = Object.fromEntries(formData)
     // const type = data['type']
     // const playerNumber = Number.parseFloat(data['player-number']),
     // console.log('Type: ' + type)
     // console.log('Player Number: ' + playerNumber),
     // manager.selectPlayer(playerNumber)

     manager.clearDisplay()
     // chrome.storage.local.clear()

     chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
       chrome.scripting.executeScript({
         target: { tabId: tabs[0].id },
         func: loadAllEvents
       }).then(injectionResults => {
         for (const {frameId, result} of injectionResults) {
           const events = JSON.parse(result)['events']
           for (event of events) {
             const key = `${event.date}_${event.home}_${event.away}`.toUpperCase()
             const json = { [key]: event }
             chrome.storage.local.set(json)
           }
         }
       })
       chrome.scripting.executeScript({
         target: { tabId: tabs[0].id },
         func: logEvento
       }).then(injectionResults => {
         for (const {frameId, result} of injectionResults) {
           const events = JSON.parse(result)['events']
           for (event of events) {
             manager.logMessage('aaa' + JSON.stringify(event))
             const key = `${event.date}_${event.home}_${event.away}`.toUpperCase()
             chrome.storage.local.get(key).then(result => {
               manager.logMessage('bbb' + JSON.stringify(result[key]))
               const event_final = {...event, ...result[key]}
               manager.logMessage('ccc' + JSON.stringify(event_final))
               const json = { [key]: event_final }
               chrome.storage.local.set(json)
             })
           }
         }
       })
     })

     console.log("Date,Hour,Country,League,Home,Away")
     chrome.storage.local.get(null).then(results => {
       for (const [key, value] of Object.entries(results)) {
         manager.logMessage(`${key}: ${JSON.stringify(value)}`)
       }
     })


     function logEvento() {

       function getData() {
         const data_field = document.getElementsByClassName('ml-0 my-0 py-0 px-0 text-slate-200')
         const data_values = data_field[0].innerText.split("/")
         const data = `${data_values[2]}-${data_values[1]}-${data_values[0]}`
         return data
       }
    
       function loadEvento(evento) {
         console.log(evento.innerText)
         const home = document.getElementsByClassName('text-center break-words p-1')[0].innerText
         const away = document.getElementsByClassName('text-center break-words p-1')[1].innerText
         const scoreElement = document.getElementsByClassName('flex flex-row items-center justify-center')
        
         let scoreHome = ''
         let scoreAway = ''
         let score = ''
         let elemento_status = document.getElementsByClassName('flex flex-row items-center justify-center')
         if (elemento_status.length > 0) {
           let status = elemento_status[0].innerText
           if (scoreElement.length == 2 && status == "FINALIZADO") {
               scoreValue = document.getElementsByClassName('flex flex-row items-center justify-center')[1].innerText
               scoreHome = scoreValue.split("\n\n")[0]
               scoreAway = scoreValue.split("\n\n")[1]
               score = scoreValue.replace("\n\n", "x")
           }
         }
            
         const tbody = document.getElementsByTagName('tbody')
         const linhas = tbody[0].childNodes
    
         let event = {}
         for (const linha of linhas) {
             let placar = linha.childNodes[0].innerText
             let probabilidade = linha.childNodes[2].innerText.replace("%", "")
             if (placar == 'Goleada do Mandante') {
                 placar = 'AOHW'
             } else if (placar == 'Goleada do Visitante') {
                 placar = 'AOAW'
             } else if (placar == 'Qualquer Outro Empate') {
                 placar = 'AOD'
             }
             event[placar] = probabilidade
         }
         event['date'] = data
         event['home'] = home
         event['away'] = away
         event['ScoreHome'] = scoreHome
         event['ScoreAway'] = scoreAway
         event['Score'] = score
         return event
       }
    
       const data = getData()
    
       const eventos = document.getElementsByClassName('cursor-pointer hover:bg-green-500 hover:text-white px-5 py-4')
       const events = []
       for (const evento of eventos) {
         evento.click()
         const event = loadEvento(evento)
         events.push(event)
       }
       return JSON.stringify({ 'events': events });
     }
    
     function loadAllEvents() {
       function getData() {
         const data_field = document.getElementsByClassName('ml-0 my-0 py-0 px-0 text-slate-200')
         const data_values = data_field[0].innerText.split("/")
         const data = `${data_values[2]}-${data_values[1]}-${data_values[0]}`
         return data
       }
    
       const data = getData()
      
       const paises = document.getElementsByClassName('mt-8')
       
       const events = []
       for (let pais of paises) {
           let paisNome = pais.childNodes[0].innerText
           let ligas = pais.childNodes[1].getElementsByClassName('mb-4')
           for (let liga of ligas){
               let ligaNome = liga.childNodes[0].childNodes[0].childNodes[0].innerText
               let eventos = liga.childNodes[0].childNodes[0].childNodes[1].childNodes
               eventos.forEach((evento) => {
                   evento.click();
    
                   debounce(20000, async (event) => {
                     evento.click();
                   })
    
                   let scoreHome = ''
                   let scoreAway = ''
                   let score = ''
                   let elemento_status = document.getElementsByClassName('flex flex-row items-center justify-center')
                   if (elemento_status.length > 0) {
                     let status = elemento_status[0].innerText
                     const scoreElement = document.getElementsByClassName('flex flex-row items-center justify-center')
                     if (scoreElement.length == 2 && status == "FINALIZADO") {
                         scoreValue = document.getElementsByClassName('flex flex-row items-center justify-center')[1].innerText
                         scoreHome = scoreValue.split("\n\n")[0]
                         scoreAway = scoreValue.split("\n\n")[1]
                         score = scoreValue.replace("\n\n", "x")
                     }
                   }
    
                   let eventoNome = evento.innerText
                   let horaEvento = eventoNome.split(' - ')[0]
                   let home = eventoNome.split(' - ')[1].split(' x ')[0]
                   let away = eventoNome.split(' - ')[1].split(' x ')[1]
                   events.push({
                     scoreHome: scoreHome,
                     date: data,
                     hour: horaEvento,
                     country: paisNome,
                     league: ligaNome,
                     home: home,
                     away: away,
                   })
               })
           }
       }
       return JSON.stringify({ 'events': events });
     }
    
 })
