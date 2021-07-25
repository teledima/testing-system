$('#all-tests tr:not(.table-head)').on('click', function(e) {
	if ($(this).hasClass('selected'))
	{
	    $(this).removeClass('selected');
	    $("input[type='submit']").prop('disabled', true);
	}
	else
	{
		$('#all-tests tr.selected').removeClass('selected');
		$(this).addClass('selected');
		$("input[type='submit']").prop('disabled', false);
	}
});


$('#start-testing').on('submit', function(e) {
    $('<input>').attr({
        type: 'hidden',
        name: 'test-id',
        value: $('#all-tests tr.selected').data('id')
    }).appendTo('#start-testing');

    $('<input>').attr({
        type: 'hidden',
        name: 'action-type',
        value: 'start'
    }).appendTo('#start-testing');
});
