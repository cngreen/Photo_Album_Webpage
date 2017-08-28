//This is for the user creation form page

$(document).ready(function() {

$("form#new_user_form").submit(function(e) {
    e.preventDefault();
    var data = {}
    var Form = this;

    $.each(this.elements, function(i, v) {
        var input = $(v);
        data[input.attr("name")] = input.val();
        delete data["undefined"];
    });

    var errors = [];
    if (data['username'].length < 3) errors.push("Usernames must be at least 3 characters long");
    var re = /^\w+$/;
    if (!re.test(data['username']) && data['username'].length > 0) errors.push("Usernames may only contain letters, digits, and underscores");
    if (data['password1'].length < 8) errors.push("Passwords must be at least 8 characters long");
    if (data['password1'].replace(/\D/g,"").length < 1 || data['password1'].replace(/[^A-Z]/gi,"").length < 1) errors.push("Passwords must contain at least one letter and one number");
    if (!re.test(data['password1']) && data['password1'].length > 0) errors.push("Passwords may only contain letters, digits, and underscores");
    if (!(data['password1'] === data['password2'])) errors.push("Passwords do not match");
    var ere = /\S+@\S+\.\S+/;
    if (!ere.test(data['email'])) errors.push("Email address must be valid");
    if (data['username'].length > 20) errors.push("Username must be no longer than 20 characters");
    if (data['firstname'].length > 20) errors.push("Firstname must be no longer than 20 characters");
    if (data['lastname'].length > 20) errors.push("Lastname must be no longer than 20 characters");
    if (data['email'].length > 40) errors.push("Email must be no longer than 40 characters");
    
    if (errors.length > 0) {
        $('#errorzone').empty(); 
        $.each(errors, function(i, v) {
            $("#errorzone").append('<p class="error">'+v+'</p>');
        });
   
        return;
        console.log("LOLWUT");
    }

    $.ajax({
        cache: false,
        url: secret_prefix+'/api/v1/user',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(result) {
            window.location = secret_prefix+'/login';
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
