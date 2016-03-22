$(document).ready(function() {

	// Assign click events for each sort button
	$('#name-sort').on('click', function() { sort('name'); });
	$('#owner-sort').on('click', function() { sort('owner'); });
	$('#rating-sort').on('click', function() { sort('rating'); });

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

// HTML template helper function
function createCharHtml(character) {
	return '<tr><td><a href="/char_profile/' + character.pk + '">' + character.name + '</a></td><td>' + character.owner + '</td><td>' + character.rating + '</td></tr>';
}

// Sort function called each time a sort button is pressed
function sort(param) {

	// Grab the sort icon element
	var icon_elem = $('#' + param + '-sort-icon');

	// Check to see which way we are sorting by
	var chevron_up = icon_elem.hasClass('glyphicon-chevron-up');

	// Send a post to webserver to get sorted data
	$.post('/ranking_sort', {'data': param, 'ascending': chevron_up})
	.done(function(data) {

		// Parse out character data from returned JSON
		var characters = data["characters"];

		// Clear the table body HTML
		$('#character-table-body').html('');

		// Append the characters to the table
		for(var i = 0; i < characters.length; i++) {
			$('#character-table-body').append(createCharHtml(characters[i]));
		}

		// Change direction of chevron
		if(chevron_up) {
			icon_elem.removeClass('glyphicon-chevron-up');
			icon_elem.addClass('glyphicon-chevron-down');
		} else {
			icon_elem.removeClass('glyphicon-chevron-down');
			icon_elem.addClass('glyphicon-chevron-up');
		}
	});
}