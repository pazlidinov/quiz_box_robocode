var sec = document.getElementById("clock").value;
function pad(val) { return val > 9 ? val : "0" + val; }
setInterval(function () {
    document.getElementById("seconds").innerHTML = pad(--sec % 60);
    document.getElementById("minutes").innerHTML = pad(parseInt(sec / 60, 10));
    document.getElementById("clock").value=sec

    clock=document.getElementById("seconds").innerHTML
    // console.log(Number(pad(--sec % 60)));
    
    if (!Number(pad(--sec % 60))){
        location.replace("/")
    }

    let answer_true = document.getElementById("true_answer")
    let ckecked_answer = document.getElementsByClassName("active")
    function updateInput(id) {
        answer_true.value=id;
    }
    updateInput(ckecked_answer[0].id)    

}, 1000);


