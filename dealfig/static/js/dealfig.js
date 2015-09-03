$(function() {
    // Dynamically add/remove fields from a form
    $(document).on('click', '.btn-add-element', function(e) {
        e.preventDefault();
        
        var controlForm = $('.controls form:first');
        var currentEntry = $(this).parents('.entry:first');
        var newEntry = $(currentEntry.clone()).appendTo($("#input-container"));
    
        newEntry.find('input').val('');
        controlForm.find('.entry:not(:last) .btn-add-element')
            .removeClass('btn-add-element').addClass('btn-remove-element')
            .removeClass('btn-success').addClass('btn-danger')
            .html('<span class="glyphicon glyphicon-minus"></span>');
    }).on('click', '.btn-remove-element', function(e) {
		$(this).parents('.entry:first').remove();
		e.preventDefault();
		return false;
	});
	
    $('.advanced-table').DataTable();
});