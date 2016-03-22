var editor;
var challenge_pk;

$(document).ready(function() {

  editor = new Quill('#basic-editor', {
    theme: 'snow'
  });
  editor.addModule('toolbar', {
    container: '#basic-toolbar'
  });
  
  if($('#challenge-pk').html()) {
    challenge_pk = $('#challenge-pk').html();
    console.log(challenge_pk);
    $('#challenge-pk').remove();
  } else {
    $('#basic-editor').remove();
    $('#basic-toolbar').remove();
    $('#submit-writing').remove();
    $('#top-text').html('Error in challenge lookup!');
  }

  $('#submit-writing').on('click', function() { submit_writing(); });


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

function submit_writing() {
  html_text = editor.getHTML();
  $.post('/submit_battle', {'html': html_text, 
                'challenge': challenge_pk})
  .done(function(data) {
    $('#basic-editor').remove();
    $('#basic-toolbar').remove();
    $('#submit-writing').remove();
    $('#top-text').html('Submitted!');
    console.log(data);
  });
}