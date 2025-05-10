//focus.js

const start = document.querySelector('.wstart');


if(start){
start.addEventListener('click', function (){
    const header = document.querySelector('header'); const hcontent1 = document.querySelector('.hm'); const hcontent2 = document.querySelector('.hsu'); const hcontent3 = document.querySelector('.menus');
    const ribon = document.querySelector('.subhead'); 
    // Start fullscreen
    if(!document.fullscreenElement){
    document.body.requestFullscreen().then(() => {
        console.log('!J Fullscreen started');
        document.body.classList.add('fullscreen');
        hcontent1.style.display = 'none';
        hcontent2.style.display = 'none';
        header.style.display = 'none';
        hcontent3.style.display = 'none';
        ribon.style.display = 'none';
        
        

        // change the start button to finish button
        start.style.display = 'none';
    }).catch(err => {
        console.error('!J Failed to enter fullscreen mode:',err);
    });
}
});}


function requestFullscreen(element) {
    if (element.requestFullscreen) {
        element.requestFullscreen();
    } else if (element.mozRequestFullScreen) { // Firefox
        element.mozRequestFullScreen();
    } else if (element.webkitRequestFullscreen) { // Safari
        element.webkitRequestFullscreen();
    } else if (element.msRequestFullscreen) { // IE/Edge
        element.msRequestFullscreen();
    } else {
        console.error('Fullscreen API is not supported in this browser.');
    }
}

//clock
function clock(){
    let date = new Date();
    let year = date.getFullYear();
    let mon = date.getMonth()+1;
    let day = date.getDate();
    let sdy = date.getDay();
    let hou = date.getHours();
    let min = date.getMinutes();


    if(sdy===1){sdy='月';}if(sdy===2){sdy='火';}if(sdy===3){sdy='水';}if(sdy===4){sdy='木';}if(sdy===5){sdy='金';}if(sdy===6){sdy='土';}if(sdy===0){sdy='日';}
    if(hou<10){hou = "0" + hou;}if(min<10){min = "0" + min;}

    let info_d = year+"年"+mon+"月"+day+"日"+sdy+"曜日"+ "¥n" +hou+":"+min;
   
    let clo = document.getElementById('timespace');
    clo.innerHTML=info_d;
}
setInterval('clock()',1000);