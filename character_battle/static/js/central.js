$(document).ready(function() {
  $('#challenging').on('click', function() { challenging(); });
  $('#challenger').on('click', function() { challenger(); });
  $('#battles').on('click', function() { battles(); });
  $('#search').on('keypress', function() { get_chars(event, this); })

  $("#menu-toggle").click(function(e) {
      e.preventDefault();
      $("#wrapper").toggleClass("toggled");
  });

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });

  $.get("/challenging")
      .done(function( data ) {
        console.log("finished")
        $( ".option" ).remove()
        for(index in data.challenges) {
          $( ".main" ).append(data.challenges[index].html);
        }
    })

});

function challenging() {
    $.get("/challenging")
      .done(function( data ) {
        console.log("finished")
        $( ".option" ).remove()
        for(index in data.challenges) {
          $( ".main" ).append(data.challenges[index].html);
        }
    })
    .fail(function(xhrResponse, textStatus) {
      console.log(textStatus);
  });
}

function battles() {
  $.get("/battles")
    .done(function( data ) {
      console.log("finished")
      $( ".option" ).remove()
      for(index in data.challenges) {
        $( ".main" ).append(data.challenges[index].html);
      }
      $('.write').on('click', function() { write(this); });
  })
  .fail(function(xhrResponse, textStatus) {
    console.log(textStatus);
  });

}

function challenger() {
$.get("/challenger")
    .done(function( data ) {
        console.log("finished")
        $( ".option" ).remove()
        for(index in data.challenges) {
          $( ".main" ).append(data.challenges[index].html);
        }
        $('#accept').on('click', function() { accept(); })
        $('#decline').on('click', function() { decline(); })
    })
    .fail(function(xhrResponse, textStatus) {
      console.log(textStatus);
  });

}

function accept() {
  var id = $('#accept').val();
  $.get("/accept/" + id)
    .done(function( data ) {
      $.get("/battles")
        .done(function( data ) {
          console.log("finished")
          $( ".option" ).remove()
          for(index in data.challenges) {
            $( ".main" ).append(data.challenges[index].html);
          }
          $('.write').on('click', function() { write(this); });
      });
    });
}

function decline() {
  var id = $('#decline').val();
  $.get("/decline/" + id)
    .done(function( data ) {
      $.get("/challenging")
      .done(function( data ) {
        console.log("finished")
        $( ".option" ).remove()
        for(index in data.challenges) {
          $( ".main" ).append(data.challenges[index].html);
        }
    })
    });
}

function get_chars(e, t) {
  if(e.which != 13) return;
  var username = $(t).val();
  $(t).val('');
  $.get('/char_display', {username:username})
    .done(function(data) {
      $( ".option" ).remove()
      for(index in data.characters) {
        $( ".main" ).append(data.characters[index].html);
      }
      $.get('/char_dropdown')
        .done(function(data) {
          for(index in data.characters) {
            $( ".dropdown-list" ).append(data.characters[index].html);
            console.log(data.characters[index].html)
          }
          $('.challenge').on('click', function() { challenge(this); });
        });
    });
}

function challenge(t) {
  //Get challenger and challenging values
  var challenger = t.value;
  var challenging = $(t).parent('.dropdown-list').attr('value');
  
  //Post the challenge with defined vars
  $.post("/challenge", {challenger:challenger, challenging:challenging})
    .done(function( data ) {
      //When finished, head over to challenging page
      $.get("/challenging")
      .done(function( data ) {
        //Remove current option and then add new options
        $( ".option" ).remove()
        for(index in data.challenges) {
          $( ".main" ).append(data.challenges[index].html);
        }
    });
    });
}

function write(t) {
  var challenge = t.value
  $.post("/write", {'challenge':challenge})
    .done(function( data ) {

    });
}