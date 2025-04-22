//focus.js

const start = document.querySelector('.wstart');
const finish = document.querySelector('.wfinish');

const date = new Date();
const year = date.getFullYear();
const month = date.getMonth() + 1;
const day = date.getDate();
const hours = date.getHours();
const minutes = date.getMinutes();
const seconds = date.getSeconds();

if(start){
start.addEventListener('click', function (){
    const header = document.querySelector('header'); const hcontent1 = document.querySelector('.hm'); const hcontent2 = document.querySelector('.hsu'); const hcontent3 = document.querySelector('.menus');
    const ribon = document.querySelector('.subhead'); const timerContainer = document.getElementById('wtimer-container'); // タイマーエリア
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
        
        // start to work timer
        timerContainer.style.display = 'block';
        worktimer();

        // change the start button to finish button
        start.textContent = '作業終了';
        start.classList.add('wfinish');
        start.classList.remove('wstart');
    }).catch(err => {
        console.error('!J Failed to enter fullscreen mode:',err);
    });
    }else{
        document.body.exitFullscreen().then(() =>{
            document.body.classList.remove('fullscreen');
            console.log('!J Fullscreen exited');
            hcontent1.style.display = 'block';
            hcontent2.style.display = 'block';
            header.style.display = 'block';
            ribon.style.display = 'block';
            if(screen.width < 950){
                hcontent3.style.display = 'block';
            }

            // stop work timer
            stopworktimer();

            // change the finish button to start button
            start.textContent = '作業開始';
            start.classList.add('wstart');
            start.classList.remove('wfinish');
        }).catch(err => {
            console.error('!J Failed to exit fullscreen mode:',err);
        })
    }
});
}

//work timer
function worktimer(){

    let timer_current = 0;
    const timer_space = document.getElementById('wtimer');
    if(timer_space){
        timer_space.innerHTML = timer_current;
        setInterval(function(){
            timer_current++;
            timer_space.innerHTML = timer_current;
        }, 1000);
    }console.log('!J timer has started');

}

// stop the timer
function stopworktimer(){
    if(timer_interval){
        clearInterval(timer_interval);
        localStorage.setItem('worktimer', timer_current);
        timer_interval = null;
        console.log('!J timer has stopped');
    }
}

// Show data and time
/*
setInterval(function showdate(){
    let sdate = document.getElementById('clocka');
},1000);
*/