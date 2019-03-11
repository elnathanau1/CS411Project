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
      ids = data.ids[0]
      groups = data.groups[0]
      for(i = 0; i < ids.length; i++){
      // jQuery selector
        $('#list_groups_table').append('<tr><th>'+groups[i]+ids[i]+'</th></tr>')
        //$('#list_groups_table').append('<td><a href=\"https://cs411-spotify.herokuapp.com/group/'+data.ids[i]+'\"/>'+data.groups[i]+'</a></td>')

      }
    }
  });

  $('.log-out').click(function(){
    $.ajax({
      type: "GET",
      url: "/ajax/logout/",
      success: function(data) {
        alert(data[0] + " was successfully logged out");
        window.location.replace("/connect/");
      }
    });

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
              if (data.redirect) {
                  window.location.replace("/group/" + $(".group_id").val());
              }
          }
      });
  });

  // AJAX POST
  $('.join-group').click(function(){
      console.log("clicked")
      $.ajax({
          type: "POST",
          url: "/ajax/join_group/",
          dataType: "json",
          data: { "join_id": $(".join_id").val() },
          success: function(data) {
              alert(data.message);
              if (data.redirect) {
                  window.location.replace("/group/" + $(".join_id").val());
              }
          }
      });
  });

  // AJAX POST
  $('.leave-group').click(function(){
      console.log("clicked")
      $.ajax({
          type: "POST",
          url: "/ajax/leave_group/",
          dataType: "json",
          data: { "leave_id": $(".leave_id").val() },
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
