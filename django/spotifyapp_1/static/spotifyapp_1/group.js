$(document).ready(function() {

    //loaded immediately after page is done loading
    $.ajax({
        type: "GET",
        url: "/ajax/list_all_groups/",
        success: function(data) {
            console.log(data);
            for(i = 0; i < data.names.length; i++){
            // jQuery selector
            $('#all_groups_table').append('<tr><td><a id="group" href=\"https://cs411-spotify.herokuapp.com/group/'+data.ids[i]+'/\">'+data.names[i]+'</a></td></tr>')

            }
        }
    });

  // CSRF code
  function getCookie(name) {
      var cookieValue = null;
      var i = 0;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (i; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
      crossDomain: false, // obviates need for sameOrigin test
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type)) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

});
