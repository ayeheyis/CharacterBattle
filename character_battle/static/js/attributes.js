var picked = [-1, -1, -1]

$(document).ready(function() {
    //Create handlers for buttons clicks
    $('#save').on('click', function() { save(); });
    $('.options').click(function() { pick(this); });

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

function pick(t) {
  var attr_id = t.value;
	var index;
  if((index = picked.indexOf(attr_id)) != -1) {//Check if there is spot a left
      picked[index] = -1;
      $( '#' + index ).remove();
      return;
  }
  if((index = picked.indexOf(-1)) == -1) return; //List is full

  //add and post
	$.post('/pick', {attr_id: attr_id})
		.done(function(data) {
		    picked[index] = attr_id;
        //Creates html format for data
		    var header =  "<h2 class='text-center'>" + data[0].fields.title + "(" + data[0].fields.rating + ")</h2>\n";
        var image = '';

        if(data[0].fields.image != null && data[0].fields.image != "") {
          image = "<img src='/attr_media/" + data[0].pk + "'>\n";
        }
        var caption = "<div class='caption'>\n <p>" + data[0].fields.description + "</p>\n</div>\n";
        var top = "<div id='" + index + "' class='col-md-3 attrs'>\n <div class='thumbnail'>\n";
		    var bottom = "</div>\n </div>";
		    var html = top + header + image + caption + bottom;
        //Adds ele to  dom
		    $( "#choose" ).after( html );

        //Performs animations
		    var bounce = new Bounce();
          bounce.scale({
            from: { x: 0.1, y: 0.1 },
            to: { x: 1, y: 1 },
            duration: 2000,
            easing: "bounce",
            delay: 100,
            stiffness: 1,
            bounces: 10
          });
          bounce.applyTo($("#" + index));
		});
}

function save() {
  //Checks if exactly 3 attrs were picked
  if(picked.indexOf(-1) != -1) return;
  //Gets attr ids
  var char_id = $('#char_id').val();
  var first = picked[0];
  var second = picked[1];
  var third = picked[2];
  //Saves by sending a post alongside the 3 attrs pk
  $.post('/save_attr', {first:first, second:second, third:third, char_id:char_id})
	.done(function(data) {
    //Adds finished button
    $( '#save_form' ).remove();
    var html = "<a href='/'class='btn btn-success btn-lg btn-block'>Finished</a>"
    $( ".list-group" ).after( html );
    //Creates animation for attr thumbnails
    var bounce = new Bounce();
    bounce.rotate({
      from: 0,
      duration: 2000,
      to: 360
    });
    bounce.applyTo($(".attrs"));
	});
}