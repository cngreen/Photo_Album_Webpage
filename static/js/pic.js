//This is for the pic viewing page

function load_data() {
    $.get(secret_prefix+"/api/v1/pic/<picid>", function(data) {
       username = data.username;
       $("#update_caption_input").val(data.caption);
       $("#next").val(data.next);
       $("#prev").val(data.prev);
       $("#picid").val(data.picid)
       $("#format").val(data.format)
       $("albumid").val(data.albumid)
    }, 'json');
}


$(document).ready(function() {

load_data()

$("form#new_caption").submit(function(e) {
    e.preventDefault();
    var data = {}
    var Form = this;


    $.each(this.elements, function(i, v) {
        var input = $(v);
        data[input.attr("caption")] = input.val();
        delete data["undefined"];
        $("#btn1").onclick(function(){
            $("#caption").val(+v.caption+); //Need to get new caption and insert via this button
        });
    });

    $.ajax({
        cache: false,
        url: secret_prefix+'/api/v1/pic',
        type: 'PUT',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(result) {
            window.location = secret_prefix+'/'+picid;
        },
        error: function(xhr, text, error) {
            var errors = $.parseJSON(xhr.responseText).errors;
            $('#errorzone').empty(); 
            $.each(errors, function(i, v) {
                $("#errorzone").append('<p class="error">'+v.message+'</p>');
            });
        }
    });

});

});