const AUTOCLOSE = true;

document.addEventListener('DOMContentLoaded', function() {
    checkIsLogged();

    $('form').on('submit', function(e){
          e.preventDefault();
    });
});

btnLogin.addEventListener("click", () => {
    sendUsers();
});

btnLogout.addEventListener("click", () => {
    resetUser();
    closePopup()
});

btnExercise.addEventListener("click", () => {

    createMessage(true).then(function() {
        closePopup();
    });
});

function resetUser(){

    chrome.alarms.clearAll();
    chrome.storage.sync.set({ 'token': null }, function(){
        console.log('Deslogado!');
        checkIsLogged();
    });
}

function sendUsers(){
    chrome.alarms.clearAll();
    let user = document.getElementById("lblUser").value;
    let pass = document.getElementById("lblPass").value;
    let cryptedPass = md5(pass);
    let url = "http://fifit.com.br";
    url = url + "/api/login?usuario=" + user + "&" + "senha=" + cryptedPass;

    $.getJSON(url, function( response ) {
        console.log(response);
        storeTokenAndFirst(response);
        createMessage(false).then(function() {
            closePopup();
        });
    }).fail(
        function() { console.log("Erro no login!"); 
    });
}

function storeTokenAndFirst(jsonReceived){
    if(jsonReceived['status'] === 200){
        console.log("Logado! Salvando token...");
    }
    else{
        console.log("erro: " + jsonReceived['error']);
    }
    let token = jsonReceived["token"];
    let hora_inicio = jsonReceived["hora_inicio"];
    let hora_final = jsonReceived["hora_final"];
    chrome.storage.sync.set({ 'token': token, 'hora_inicio': hora_inicio , 'hora_final': hora_final}, function(){
        console.log(jsonReceived);
        console.log('Login realizado!');
    });
}

async function createMessage(automatic){

    let hora_inicio = await chrome.storage.sync.get(['hora_inicio']);
    hora_inicio = hora_inicio["hora_inicio"];
    let hora_final = await chrome.storage.sync.get(['hora_final']);
    hora_final = hora_final["hora_final"];

    let hora_atual = parseInt(new Date().toLocaleString('pt-BR', { hour: 'numeric', hour12: false }));

    // se estiver no horario estipulado envia mensagem
    if(hora_inicio <= hora_atual && hora_atual <= hora_final){

        console.log("Exercício disponível!");
        chrome.runtime.sendMessage({breaktime: "exercise"});
    }else{
        if (automatic){
            await alert("Exercício indisponível!");
        }
        console.log("Exercício indisponível!");
    }
}

async function checkIsLogged(){

    let token = await chrome.storage.sync.get(["token"]);
    token = token["token"];

    if (token){
        $("#divLogout").show();
        $("#divLogin").hide();
    }
}

function closePopup(){
    
    if (AUTOCLOSE){
        window.close();
    }
}