//This is for the user edit form page

function load_data() {
    $.get(secret_prefix+"/api/v1/user", function(data) {
       username = data.username;
       $("#update_firstname_input").val(data.firstname);
       $("#update_lastname_input").val(data.lastname);
       $("#update_email_input").val(data.email);

    }, 'json');
}

$(document).ready(function() {

//Grab current user's information
load_data();

//Parse form submission
$("form#update_info_form").submit(function(e) {
    e.preventDefault();
    var data = {}
    var Form = this;

    $.each(this.elements, function(i, v) {
        var input = $(v);
        data[input.attr("name")] = input.val();
        delete data["undefined"];
    });

    var errors = [];
    var re = /^\w+$/;
    if(data['password1'].length > 0) {
        if (data['password1'].length < 8) errors.push("Passwords must be at least 8 characters long");
        if (data['password1'].replace(/\D/g,"").length < 1 || data['password1'].replace(/[^A-Z]/gi,"").length < 1) errors.push("Passwords must contain at least one letter and one number");
        if (!re.test(data['password1']) && data['password1'].length > 0) errors.push("Passwords may only contain letters, digits, and underscores");
        if (!(data['password1'] === data['password2'])) errors.push("Passwords do not match");
    }
    var ere = /\S+@\S+\.\S+/;
    
    if(data['email'].length > 0) {
        if (!ere.test(data['email'])) errors.push("Email address must be valid");
        if (data['email'].length > 40) errors.push("Email must be no longer than 40 characters");
    }
    if (data['firstname'].length > 20) errors.push("Firstname must be no longer than 20 characters");
    if (data['lastname'].length > 20) errors.push("Lastname must be no longer than 20 characters");
    
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
        type: 'PUT',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function() {
            $('#errorzone').empty(); 
            $('#update_password1_input').val("");
            $('#update_password2_input').val("");
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
