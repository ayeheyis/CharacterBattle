
var lc;

$(document).ready(function() {
	lc = LC.init(
        document.getElementsByClassName('literally')[0],
        {imageURLPrefix: '/static/img'}
    );

    $('#save-button').on('click', function() { save(); });
    $('#update-button').on('click', function() { update(); });

    if($('#lc-hidden').html()) {

    	lc.loadSnapshot(JSON.parse($('#lc-hidden').html()));
    	$('#lc-hidden').remove();
    }

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

var snap;
var snapJSON;
var image;

function save() {

	// Check for image drawn on canvas
	if(lc.getImage() == null) {
		console.log('No image');
		return;
	}

	// Get image in base64 representation
	base64string = lc.getImage().toDataURL();

	// Get an SVG string of the image
	svg = lc.getSVGString();

	// Get a JSON of the snapshot
	snapJSON = JSON.stringify(lc.getSnapshot());

	var name = $('#char-name').val();
	var desc = $('#char-desc').val();


	// AJAX call to save to database for this user
	$.post('/save_new_character', {'char_name': name, 'description': desc, 'img': base64string, 'svg_text': svg, 'snap_json': snapJSON})
		.done(function(data) {
			$('#save-button').remove();
            console.log(data)
			if($('.choose-attr-form').children().length == 0) {
				$('.choose-attr-form').append('<a href="/choose/' + data + '" class="btn btn-primary">Choose Attribute<a>');
			}
		});
}

function update() {

	// Check for image drawn on canvas
	if(lc.getImage() == null) {
		console.log('No image');
		return;
	}

	// Get image in base64 representation
	base64string = lc.getImage().toDataURL();

	// Get an SVG string of the image
	svg = lc.getSVGString();

	// Get a JSON of the snapshot
	snapJSON = JSON.stringify(lc.getSnapshot());

	var name = $('#char-name').val();
	var desc = $('#char-desc').val();
	var id = $('#char-id').val();


	// AJAX call to save to database for this user
	$.post('/update_character/' + id, {'char_name': name, 'description': desc, 'img': base64string, 'svg_text': svg, 'snap_json': snapJSON})
		.done(function(data) {
		console.log("The data is: " + data)
		});
}

function load() {

	lc.loadSnapshot(JSON.parse(snapJSON));

	$('#canvas-test').html(image);
}