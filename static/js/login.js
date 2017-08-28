//This is for the login form page

$(document).ready(function() {

//On login form submit
$("form#login_form").submit(function(e) {

    e.preventDefault();
    var data = {}
    var Form = this;

    $.each(this.elements, function(i, v) {
        var input = $(v);
        data[input.attr("name")] = input.val();
        delete data["undefined"];
    });
    $.ajax({
        cache: false,
        url: secret_prefix+'/api/v1/login',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(result) {
            var loc = getParameterByName('url',window.location);
            if (loc == null) window.location = secret_prefix+'/';
            else window.location = secret_prefix + loc;
        },
        error: function(xhr, text, error) {
            var errorslist = $.parseJSON(xhr.responseText).errors;
            $('#errorzone').empty(); 
            $.each(errorslist, function(i, v) {
                $("#errorzone").append('<p class="error">'+v.message+'</p>');
            });
        }
    });

});

});
