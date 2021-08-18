interval = setInterval(setTime, 60*1000);

$.when($.ready)
    .then(setTime);

$("input[type='submit']").on('click', function(e) {
    if ($(this).prop('id') != 'finish')
        $('<input>').attr({
                type: 'hidden',
                name: 'available-time',
                value: $('#timer').data('time')
            }).appendTo('form');
    else {
        $('#confirm-finish').dialog({
            resizable: false,
            height: 'auto',
            width: 400,
            modal: true,
            buttons: [
                {
                    text: "Да", click: function() {
                        $('<input>').attr({
                            type: 'hidden',
                            name: 'action-type',
                            value: $('#finish').prop('id')
                        }).appendTo('form');

                        $('<input>').attr({
                                type: 'hidden',
                                name: 'available-time',
                                value: $('#timer').data('time')
                        }).appendTo('form');

                        $(this).dialog('close');
                        $('form').submit();
                    }
                },
                {
                    text: "Отмена", click: function() {
                        $(this).dialog('close');
                        return false;
                    }
                }
            ]
        });
       $('#confirm-finish').dialog('open');
    }

    if ($(this).prop('id') != 'finish') {
        $('<input>').attr({
            type: 'hidden',
            name: 'action-type',
            value: $(this).prop('id')
        }).appendTo('form');
        return true;
    }
    else
        return false;
});


function setTime(){
    let minutes = $('#timer').data('time');
    if (minutes < 0) {
        clearInterval(interval);
        $('#time-ended').dialog({
            resizable: false,
            height: 'auto',
            width: 400,
            modal: true,
            buttons: [
                {
                    text:"Ок",
                    click: function(){
                        $('<input>').attr({
                            type: 'hidden',
                            name: 'action-type',
                            value: $('#finish').prop('id')
                        }).appendTo('form');

                        $('<input>').attr({
                                type: 'hidden',
                                name: 'available-time',
                                value: $('#timer').data('time')
                        }).appendTo('form');

                        $(this).dialog('close');
                        $("form").submit();
                    }
                }
            ]
        });
    }
    let hours = Math.floor(minutes / 60);
    minutes = minutes - hours * 60;
    $('#timer').text('Осталось: ' + hours == 0?(hours + ' ч.'):'' + minutes + ' мин.');
    $('#timer').data('time', minutes - 1);
}
