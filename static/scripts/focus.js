//focus.js

const start = document.querySelector('#wstart');
const finish = document.querySelector('#wfinish');

const header = document.querySelector('header'); const hcontent1 = document.querySelector('.hm'); const hcontent2 = document.querySelector('.hsu'); const hcontent3 = document.querySelector('.menus');
const ribon = document.querySelector('.subhead'); const exitonly1 = document.querySelector('.fullsc1'); const exitonly2 = document.querySelector('.fullsc2'); const footers = document.querySelector('.f_el');
/*
const date = new Date();
const year = date.getFullYear();
const month = date.getMonth() + 1;
const day = date.getDate();
let sdy = date.getDay();
let hours = date.getHours();
let minutes = date.getMinutes();
let seconds = date.getSeconds();
*/
if(start){
start.addEventListener('click', function (){

    // Start fullscreen
    if(!document.fullscreenElement){
    enterFullscreen(document.documentElement).then(() => {
        console.log('!J Fullscreen started');
        //document.body.classList.add('fullscreen');
        hcontent1.style.display = 'none';
        hcontent2.style.display = 'none';
        header.style.display = 'none';
        hcontent3.style.display = 'none';
        ribon.style.display = 'none';
        footers.style.display = 'none';
        exitonly1.style.display = 'block';
        exitonly2.style.display = 'block';
        startClock();
        

    }).catch(err => {
        console.error('!J Failed to enter fullscreen mode:',err);
    });
    }
});
}if(finish){
    finish.addEventListener('click',function(){
    
        document.body.exitFullscreen().then(() => {
            //document.body.classList.remove('fullscreen');
            console.log('!J Fullscreen exited');
            hcontent1.style.display = 'block';
            hcontent2.style.display = 'block';
            header.style.display = 'block';
            ribon.style.display = 'block';
            footers.style.display = 'block';
            exitonly1.style.display = 'none';
            exitonly2.style.display = 'none';
            if(screen.width < 950){
                hcontent3.style.display = 'block';
            }
            stopClock();

        }).catch(err => {
            console.error('!J Failed to exit fullscreen mode:',err);
        });
    });
}
document.addEventListener('fullscreenchange',()=>{
    if(!document.fullscreenElement){
        exitFullscreen();
        console.log('!J Fullscreen exited');
        hcontent1.style.display = 'block';
        hcontent2.style.display = 'block';
        header.style.display = 'block';
        ribon.style.display = 'block';
        footers.style.display = 'block';
        exitonly1.style.display = 'none';
        exitonly2.style.display = 'none';
        if(screen.width < 950){
            hcontent3.style.display = 'block';
        }
        stopClock();
        location.reload();
    }
});

// enter fullscreen
function enterFullscreen(element){
    if(element.requestFullscreen){
        return element.requestFullscreen();
    }else if(element.mozRequestFullScreen){
        return element,mozRequestFullScreen();
    }else if(element.webkitRequestFullscreen){
        return element.webkitRequestFullscreen();
    }
}

// exit fullscreen
function exitFullscreen(){
    if(document.exitFullscreen){
        return document.exitFullscreen();
    }else if(document.mozCancelFullScreen){
        return document.mozCancelFullScreen();
    }else if(document.webkitExitFullscreen){
        return document.webkitExitFullscreen();
    }
}
// A function of the start clock
function startClock(){
// clocks
const showtime = document.getElementById('timespace');
if(!showtime) return;

ctimeInterval = setInterval(() => {
    const date = new Date();
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    let sdy = date.getDay();
    let hours = date.getHours();
    let minutes = date.getMinutes();
    let seconds = date.getSeconds();
    if(sdy===1){sdy='月';}if(sdy===2){sdy='火';}if(sdy===3){sdy='水';}if(sdy===4){sdy='木';}if(sdy===5){sdy='金';}if(sdy===6){sdy='土';}if(sdy===0){sdy='日';}
    if(hours<10){hours = "0" + hours;}if(minutes<10){minutes = "0" + minutes;}if(seconds<10){seconds = "0" + seconds;}

    //let current_time = `${year}年${month}月${day}日${sdy}曜日 <br> ${hours}:${minutes}:${seconds}`;
    let current_time = year + "年" + month + "月" + day + "日" + sdy + "曜日 <br> " + hours + ":" + minutes + ":" + seconds;
    showtime.innerHTML = current_time;
},1000);
}

// A function of the stop clock when exit the fullscreen
function stopClock(){
    if(ctimeInterval){
        ctimeInterval = null;
        console.log('!J Clock has stopped');
    }
}