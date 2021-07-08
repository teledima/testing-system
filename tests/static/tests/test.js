interval = setInterval(setTime, 60*1000);

$.when($.ready)
    .then(setTime);


function setTime(){
    let minutes = $('#timer').data('time');
    if (minutes < 0) {
        alert('End');
        clearInterval(interval);
        return;
    }
    let hours = Math.floor(minutes / 60);
    minutes = minutes - hours * 60;
    $('#timer').text('Осталось: ' + hours == 0?(hours + ' ч.'):'' + minutes + ' мин.');
    $('#timer').data('time', minutes - 1);
}