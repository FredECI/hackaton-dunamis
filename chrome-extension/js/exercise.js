document.getElementById("start_counter").addEventListener("click", function(){
    
    clockActivated();
});

function clockActivated() {

    let data_atual = getDataHoje();

    chrome.storage.sync.set({ 'last_exercise': data_atual }, function(){
        console.log('Cronômetro iniciado!');
    });
}


function getDataHoje(){
  
    return new Date().toLocaleString('pt-BR', { day: 'numeric', month: 'numeric', year: 'numeric', hour12: false });
}