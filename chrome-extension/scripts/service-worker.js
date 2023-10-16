chrome.commands.onCommand.addListener((command,tab) => {
    chrome.tabs.query({ currentWindow: true, active: true })
    .then((tabs) => {
        if (command == "load-results-from-event") {
            chrome.scripting.executeScript({
                target: { tabId: tabs[0].id},
                func: logEvento
            });
        } else if (command == "load-all-events") {
            chrome.scripting.executeScript({
                target: { tabId: tabs[0].id},
                func: loadAllEvents
            });
        } else if (command == "load-header") {
            chrome.scripting.executeScript({
                target: { tabId: tabs[0].id},
                func: loadHeaderEvent
            });
        }
    })
});

function loadAllEvents() {
    function adicionaZero(numero){
        if (numero <= 9) 
            return "0" + numero;
        else
            return numero; 
    }

    console.log("Date;Hour;Country;League;Home;Away");
    const paises = document.getElementsByClassName('mt-8')
    for (let pais of paises) {
        let paisNome = pais.childNodes[0].innerText
        let ligas = pais.childNodes[1].getElementsByClassName('mb-4')
        for (let liga of ligas){
            let ligaNome = liga.childNodes[0].childNodes[0].childNodes[0].innerText
            let eventos = liga.childNodes[0].childNodes[0].childNodes[1].childNodes
            eventos.forEach((evento) => {
                let eventoNome = evento.innerText
                let horaEvento = eventoNome.split(' - ')[0]
                let home = eventoNome.split(' - ')[1].split(' x ')[0]
                let away = eventoNome.split(' - ')[1].split(' x ')[1]
                const date = new Date();
                let data = date.getFullYear() + '-' + adicionaZero(date.getMonth() + 1) + '-' + adicionaZero(date.getDate())
                let logEvento = data+';'+horaEvento+';'+paisNome+';'+ligaNome+';'+home+';'+away;
                console.log(logEvento);
            });
        }
    }
}

function loadHeaderEvent() {
    console.log('Home;Away;ScoreHome;ScoreAway;Score;0x0;0x1;0x2;0x3;1x0;1x1;1x2;1x3;2x0;2x1;2x2;2x3;3x0;3x1;3x2;3x3;AOAW;AOD;AOHW')
}

function logEvento() {
    const home = document.getElementsByClassName('text-center break-words p-1')[0].innerText
    const away = document.getElementsByClassName('text-center break-words p-1')[1].innerText
    const scoreElement = document.getElementsByClassName('flex flex-row items-center justify-center')
    
    let scoreHome = '';
    let scoreAway = '';
    let score = '';
    let status = document.getElementsByClassName('flex flex-row items-center justify-center')[0].innerText
    if (scoreElement.length == 2 && status == "FINALIZADO") {
        scoreValue = document.getElementsByClassName('flex flex-row items-center justify-center')[1].innerText
        scoreHome = scoreValue.split("\n\n")[0]
        scoreAway = scoreValue.split("\n\n")[1]
        score = scoreValue.replace("\n\n", "x")
    }
    
    const tbody = document.getElementsByTagName('tbody')
    const linhas = tbody[0].childNodes

    let resultados = [];
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
        resultados.push({'placar': placar, 'probabilidade': probabilidade})
    }
    resultados = resultados.sort((x, y) => (x.placar > y.placar ? 1 : -1))
    let logEvento = home+';'+away+';'+scoreHome+';'+scoreAway+';'+score;
    resultados.forEach((resultado) => {
        logEvento += (';'+resultado.probabilidade);
    });
    console.log(logEvento);
}