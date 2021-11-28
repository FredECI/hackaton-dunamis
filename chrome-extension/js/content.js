canExercise();

randomAlarm();

async function canExercise(){
    let token = await chrome.storage.sync.get(["token"]);
    token = token["token"];
    let last_exercise = await chrome.storage.sync.get(["last_exercise"]);
    last_exercise = last_exercise["last_exercise"];

    let data_atual = new Date().toLocaleString('pt-BR', { day: 'numeric', month: 'numeric', year: 'numeric', hour12: false });
    
    if (token && (last_exercise || stringToDate(last_exercise) < stringToDate(data_atual))){

        let url = "http://fifit.com.br";
        url = url + "/api/tempo?token=" + token;
        
        $.getJSON(url, function( response ) {
            let hora_inicio = response["hora_inicio"];
            let hora_final = response["hora_final"];
            chrome.storage.sync.set({ 'hora_inicio': hora_inicio, 'hora_final': hora_final }, function(){
                console.log(response);
                console.log('Update realizado!');
            });
        }).fail(function() { console.log("Falha no update!"); });
    }
    else{
        console.log("Exercício indisponível!");
    }
}


async function randomAlarm(){

    let next_date = await chrome.storage.sync.get(["next_date"]);
    next_date = next_date["next_date"];

    let data_atual = new Date().toLocaleString('pt-BR', { day: 'numeric', month: 'numeric', year: 'numeric', hour12: false });
    
    if (!next_date){
        // cria primeira vez
        setNewDateRandomMessage();
        console.log('criado novo');
        return;
    }
    else if (stringToDate(next_date) <= stringToDate(data_atual)){
        
        console.log('is on date next: ' + next_date + ' atual: ' + data_atual);
        let url = "http://fifit.com.br";
        url = url + "/api/mensagem";
        
        $.getJSON(url, function( response ) {
            let rand_msg = response["mensagem"];
            chrome.storage.sync.set({ 'rand_msg': rand_msg }, function(){
                console.log(response);
                setNewDateRandomMessage();
                chrome.runtime.sendMessage({alarm: "random_message"});
            });
        }).fail(function() { console.log("Falha no alerta aleatório!"); });
    }
}


function setNewDateRandomMessage(){
    
    var next_date = RandomDayfromToday(3, 7)
    chrome.storage.sync.set({ 'next_date': next_date });
    console.log('Alerta aleatório criado para ' + next_date + '!');
}


function RandomDayfromToday(daysMin, daysMax) {

    var days = Math.floor(Math.random() * (daysMax - daysMin + 1)) + daysMin;
    var result = new Date();
    result.setDate(result.getDate() + days);
    return result.toLocaleString('pt-BR', { day: 'numeric', month: 'numeric', year: 'numeric', hour12: false });
}


function stringToDate(strDate){
    if(!strDate) return undefined;
    var parts = String(strDate).split("/");
    return new Date(parts[2], parts[1] - 1, parts[0]);
 }