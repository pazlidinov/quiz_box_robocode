var sec = 120;
function pad(val) { return val > 9 ? val : "0" + val; }
setInterval(function () {
    document.getElementById("seconds").innerHTML = pad(--sec % 60);
    document.getElementById("minutes").innerHTML = pad(parseInt(sec / 60, 10));
    document.getElementById("clock").value = sec

    clock = document.getElementById("seconds").innerHTML


    if (!Number(pad(--sec % 60))) {
        location.replace("/")
    }
}, 1000);


