$(document).ready(function() {
    $('.img-bg-color').hover( function() { handlerIn(this); }, function() { handlerOut(this); } )

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

});

function handlerIn(t) {
    var bounce = new Bounce();
    bounce.scale({
      from: { x: 1, y: 1 },
      to: { x: .5, y: .5 },
      duration: 2000,
      easing: "bounce",
      delay: 0,
      stiffness: 1,
      bounces: 10
    });
    var id = t.id;
    bounce.applyTo($("#" + id));
}

function handlerOut(t) {
var bounce = new Bounce();
    bounce.scale({
      from: { x: .5, y: .5 },
      to: { x: 1, y: 1 },
      duration: 2000,
      easing: "bounce",
      delay: 0,
      stiffness: 1,
      bounces: 10
    });
    var id = t.id;
    bounce.applyTo($("#" + id));
}
