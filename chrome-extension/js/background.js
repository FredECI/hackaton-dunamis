chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    
    if (request.breaktime === "exercise"){

      // chrome
      createRedirect("exercise");
    }

    if (request.alarm === "random_message"){
      
      // alarm 
      showAlarm();
    }
  }
);

async function createRedirect(page){
  
  let token = await chrome.storage.sync.get(["token"]);
  token = token["token"];
  if(token){
    chrome.windows.create({
      state: "maximized",
      url: "http://fifit.com.br/" + page + "?token=" + token,
      focused: true
    });
  }
}

async function showAlarm(){
  
  let rand_msg = await chrome.storage.sync.get(["rand_msg"]);
  
  if (rand_msg["rand_msg"]){
    rand_msg = rand_msg["rand_msg"];
  }
  else{
    rand_msg = "Hora de se exercitar, né?";
  }
  chrome.notifications.create(createNotification(rand_msg));
}

function createNotification(text){
    
  return {
      title: 'FiFit',
      message: text,
      iconUrl: '/images/fifit_logo_preg_48.png',
      type: 'basic'
  }
}

function getDataHoje(){
  
  return new Date().toLocaleString('pt-BR', { day: 'numeric', month: 'numeric', year: 'numeric', hour12: false });
}