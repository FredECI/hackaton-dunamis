var score = 0;
var isTracking = false;
var counter = document.getElementById("start_counter")

counter.addEventListener("click", function(){
    isTracking = true;
    var audio = new Audio("/assets/audio/relaxed-guitar.mp3");
    audio.loop = true;
    audio.play();
    counter.style.display="none";
});

// Add event listener on keydown
document.addEventListener('keydown', (event) => {

    if (! isTracking) return;
    console.log("code: " + event.code + " key: " + event.key);
    // Alert the key name and key code on keydown
    switch(event.code){
        
        case "F5":
            score = score += 50;
            break;
        case "F1":
        case "F2":
        case "F3":
        case "F4":
        case "F6":
        case "F7":
        case "F8":
        case "F9":
        case "F10":
        case "F11":
        case "F12":
        case "AltLeft":
        case "AltRight":
        case "ControlLeft":
        case "ControlRight":
        case "ShiftLeft":
        case "ShiftRight":
        case "CapsLock":
        case "Enter":
        case "Tab":
        case "Backspace":
        case "NumpadEnter":
        case "ContextMenu":
            score = score += 30;
            break;
        default:
            score = score += 2;
    }
    event.preventDefault();
}, false);

document.body.addEventListener("mousemove", function(event) {
    
    if (! isTracking) return;
    score = score += 0.02;
    console.log("mousemoved");
});

document.addEventListener("visibilitychange", function (event){
    
    if (! isTracking) return;
    document.visibilityState === 'visible'
    console.log(event)
    console.log('FECHOU ESSA MERDA!');
});