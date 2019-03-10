$(document).ready(function() {

  //loaded immediately after page is done loading
  $.ajax({
    type: "GET",
    url: "/ajax/top_artists/",
    success: function(data) {
      for(i = 0; i < data.length; i++){
      // jQuery selector
        $('#top_artist_table').append('<tr><th>'+data[i]+'</th></tr>')
      }
    }
  });

  //loaded immediately after page is done loading
  $.ajax({
    type: "GET",
    url: "/ajax/list_groups/",
    success: function(data) {
      for(i = 0; i < data.length; i++){
      // jQuery selector
        $('#list_groups_table').append('<tr><th>'+data[i]+'</th></tr>')
      }
    }
  });

  // AJAX POST
  $('.create-group').click(function(){
      console.log("clicked")
      $.ajax({
          type: "POST",
          url: "/ajax/create_group/",
          dataType: "json",
          data: { "new_id": $(".group_id").val(), "new_name": $(".group_name").val() },
          success: function(data) {
              alert(data.message);
          }
      });

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
