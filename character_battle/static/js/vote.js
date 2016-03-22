$(document).ready(function() {


  $('.submit-vote').on('click', function() { submit_vote(this); });


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

function submit_vote(b) {

  s = $(b).attr('id').split('-');
  battle_id = parseInt(s[0]);
  character_id = parseInt(s[1]);

  $.post('/vote', {'battle': battle_id, 'character': character_id})
  .done(function(data) {
    location.reload();
  });

}