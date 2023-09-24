
let answer = document.querySelectorAll("#javoblar");
let answer_true = document.getElementById("true_answer")


function checkAnswer(answerElement){
    answer_true.setAttribute("id", answerElement.getAttribute("data-answer-id"))
   
}


answer.forEach(el =>{    
    el.onclick = checkAnswer(el);
})





// timer 
// var sec = document.getElementById("clock").value * 60;
// function pad(val) { return val > 9 ? val : "0" + val; }
// setInterval(function () {
//     document.getElementById("seconds").innerHTML = pad(--sec % 60);
//     document.getElementById("minutes").innerHTML = pad(parseInt(sec / 60, 10));
//     document.getElementById("clock").value = sec

//     clock = document.getElementById("seconds").innerHTML
// }, 1000);

// function startTimer(duration, display) {
//     var timer = duration, minutes, seconds;
//     setInterval(function () {
//         sessionStorage.setItem("time",display.textContent )
//         minutes = parseInt(timer / 60, 10);
//         seconds = parseInt(timer % 60, 10);

//         minutes = minutes < 10 ? "0" + minutes : minutes;
//         seconds = seconds < 10 ? "0" + seconds : seconds;

//         display.textContent = minutes + ":" + seconds;
     
//         if (--timer < 0) {
//             timer = duration;
//         }
//     }, 1000);
// }

// display = document.querySelector('#time');
// let minute = parseInt(sessionStorage.getItem("time").split(":")[0])
// let seconds = parseInt(sessionStorage.getItem("time").split(":")[1])
// var time = (minute*60) + seconds

// window.onload = function () {
//     console.log(minute,seconds)
//     if(minute && seconds){
//         startTimer(time, display);
//     }else{
//         startTimer(600, display);
//     }
    
// };

//<h4 class="h4 mx-2 my-3"><span id="minutes"></span>:<span id="seconds"></span></h4>