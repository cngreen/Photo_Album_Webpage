window.onpopstate = function(event) {
  if(event.state.type === "pic") {
    show_pic(event.state.id, false);
  }
  else if(event.state.type === "album") {
    show_album(event.state.id, false);
  }
}

function update_caption(picid) {
  $.ajax({
      cache: false,
      url: secret_prefix+'/api/v1/pic/'+picid,
      type: 'PUT',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({'caption': $("#captioninput").val()}),
      error: function(xhr, text, error) {
          var errorslist = $.parseJSON(xhr.responseText).errors;
          $('#errorzone').empty();
          $.each(errorslist, function(i, v) {
              $("#errorzone").append('<p class="error">'+v.message+'</p>');
          });
      }
  });
}

function show_pic(picid, shouldPush) {
  if(shouldPush) history.pushState({type: "pic", id: picid}, "", secret_prefix+"/pic?picid="+picid);
  $("#errorzone").empty();
  $("#content").empty(); //goodnight
  p = picid;

  $.ajax({
    url: secret_prefix + '/api/v1/pic/' +picid,
    type: 'GET',
    success: function(result) {
      $("#errorzone").empty();

      var nextString = ''
      var prevString = ''
      if (result.next !== "")
      {
        nextString = '<a role="button" class="btn btn-primary pull-right" onClick="show_pic(`'+result.next+'`, true);">Next</a>';
      }
      else{
        nextString = '<a class="btn btn-primary disabled pull-right" role="button">Next</a>';
      }
      if (result.prev !== "")
      {
        prevString = '<a role="button" class="btn btn-primary" onClick="show_pic(`'+result.prev+'`, true);">Previous</a>';
      }
      else{
        prevString = '<a class="btn btn-primary disabled" role="button">Previous</a>';
      }

      $("#content").append('<div id="imgarea"><img class="img-responsive center-block" src="/static/images/'
          +result.picid+'.'+result.format+'"><div id="captionholder"><p id="caption">'+result.caption+'</p></div></div>'+nextString+prevString+"</div>");
      //WARNING WARNING WARNING
      $.get(secret_prefix + '/api/v1/album/' +result.albumid, function(d) {
        if(d.username === username) {
          //Do some magic to make that box appear for caption editing
          var caption = $("#caption").html();
          $("#captionholder").html("<form onsubmit='update_caption(`"+p+"`); return false;'>"+
          `<input type='text' id="captioninput" value='`+caption+`' class='form-control' placeholder="Caption your photo"></form>`);
        }
      });
      //END END END END END END
    },
    error: function(xhr, text, error) {
      var errorslist = $.parseJSON(xhr.responseText).errors;
      $.each(errorslist, function(i,v) {
        $("#errorzone").append('<p class="error">'+v.message+'</p>');
      })
    }
  });
}

function show_album(albumid, shouldPush) {
  if(shouldPush) history.pushState({type: "album", id: albumid}, "", secret_prefix+"/album?albumid="+albumid);
  $("#errorzone").empty();
  $("#content").empty(); //goodnight
  $.ajax({
    url: secret_prefix + '/api/v1/album/' +albumid,
    type: 'GET',
    success: function(result) {
      $("#errorzone").empty();

      $("#content").append('<h1>'+result.title+'</h1>');
      $("#content").append('<h4>By: '+result.username+'</h4>');
      for(var i = 0, len = result.pics.length; i < len; ++i) {
        if(i % 4 == 0) $("#content").append('<div class="row" style="text-align:center;" id="images-row-'+(i/4)+'"></div>');
        $("#images-row-"+Math.floor(i/4)).append('<div class="col-xs-12 col-sm-3"><a role="button" onClick="show_pic(`'+result.pics[i].picid+'`, true);"><img style="max-height: 240px;" src="/static/images/'
            +result.pics[i].picid+'.'+result.pics[i].format+'" class="img-responsive img-thumbnail"></a><p>'+result.pics[i].caption+
            '</p><p>'+result.pics[i].date+'</p></div>');
      }

      if (username === result.username){
        $("#content").append('<a href="'+secret_prefix+'/album/edit?albumid='+albumid+'">Edit your album</a>');
      }
    },
    error: function(xhr, text, error) {
      var errorslist = $.parseJSON(xhr.responseText).errors;
      $.each(errorslist, function(i,v) {
        $("#errorzone").append('<p class="error">'+v.message+'</p>');
      })
    }
  });
}

$(document).ready(function() {
  var thisType = window.location.pathname.split("/").pop();
  history.replaceState({type: thisType, id: getParameterByName(thisType+'id', window.location)}, "", window.location);
  $.ajax({
    url: secret_prefix + '/api/v1/user',
    type: 'GET',
    success: function(result) {
      username = result.username;
      $("#errorzone").empty();
      if(thisType === "album") show_album(getParameterByName('albumid', window.location), false);
      else if(thisType === "pic") show_pic(getParameterByName('picid', window.location), false);
    },
    error: function(xhr, text, error) {
      username = null;
      if(thisType === "album") show_album(getParameterByName('albumid', window.location), false);
      else if(thisType === "pic") show_pic(getParameterByName('picid', window.location), false);
    }
  });
});
