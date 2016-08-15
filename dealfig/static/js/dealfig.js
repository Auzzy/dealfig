$(document).ready(function() {
    // Dynamically add/remove fields from a form
    $(document).on('click', '.btn-add-element', function(e) {
        e.preventDefault();

        var controlForm = $('.controls form:first');
        var currentEntry = $(this).parents('.entry:first');
        var newEntry = $(currentEntry.clone()).appendTo($("#input-container"));

        $(newEntry).children(":text").each(function(index, element) {
            var parts = $(element).attr("name").split("-");
            var index = (parseInt(parts[1], 10) + 1).toString();
            var new_name = parts[0] + "-" + index + "-" + parts[2];
            $(element).attr("name", new_name);
        });

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

function process_uri(value) {
    value = $.trim(value);
    var matches = value.match(/^(\w+:\/\/)?\S+\.\S+$/);
    if (matches != null) {
        var protocol = matches[1];
        if (protocol === undefined) {
            return "http://" + value;
        } else {
            return value;
        }
    }
    return null;
}

function process_email(value) {
    value = $.trim(value);
    var matches = value.match(/^\S+@\S+\.\S+$/);
    if (matches != null) {
        return value;
    }
    return null;
}

function process_value(value, type) {
    if ($.type(value) == "array") {
        var new_values = $.map(value, function(val, index) {
            return process_value(val, type);
        });
        return new_values;
    } else {
        if (type === "url") {
            var uri = process_uri(value);
            if (uri != null) {
                return uri;
            }
        } else if (type === "email") {
            var email = process_email(value);
            if (email != null) {
                return email;
            }
        } else {
            return value;
        }
        return null;
    }
}