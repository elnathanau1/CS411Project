// Reorganizing and styling navigation bar

$(document).ready(function() {

    //loaded immediately after page is done loading
    $.ajax({
        type: "GET",
        url: "/ajax/get_group_members/",
        success: function(data) {
            console.log(data);
            for(i = 0; i < data.members.length; i++){
            // jQuery selector
              $('#group_members_table').append('<tr><td>'+data.members[i]+'</td></tr>')

            }
        }
    });

    //loaded immediately after page is done loading
    $.ajax({
        type: "GET",
        url: "/ajax/list_suggestions/",
        success: function(data) {
            console.log(data);
            for(i = 0; i < data.names.length; i++){
            // jQuery selector
                $('#suggestions_table').append('<tr><td>'+data.names[i]+'</td><td>'+data.artists[i]+'</td><td>'+data.genres[i]+'</td></tr>');
            }
        }
    });

    // AJAX POST
    $('.change-group-name').click(function(){
        var new_name = prompt("New name:", "default");
        if(new_name != null){
          if(new_name.length != 0){
            $.ajax({
                type: "POST",
                url: "/ajax/change_group_name/",
                dataType: "json",
                data: { "new_name": new_name },
                success: function(data) {
                  $("#name_header").text(data.group_name + " (" + data.group_id + ")");
                  // alert(data.message);
                }
            });
          }
        }
    });

    $('.leave-group').click(function(){
        console.log("clicked")
        $.ajax({
            type: "POST",
            url: "/ajax/leave_group/",
            dataType: "json",
            success: function(data) {
                alert(data.message);
                window.location.replace("/dash/");
            }
        });
    });

    $('.make-suggestions').click(function(){
        $.ajax({
            type: "POST",
            url: "/ajax/make_suggestions/",
            dataType: "json",
            success: function(data) {
              $('#suggestions_table').empty();
              for(i = 0; i < data.names.length; i++){
                  $('#suggestions_table').append('<tr><td>'+data.names[i]+'</td><td>'+data.artists[i]+'</td><td>'+data.genres[i]+'</td></tr>');
              }
          }
        });
    });

    $('.clear-suggestions').click(function(){
        $.ajax({
            type: "POST",
            url: "/ajax/clear_suggestions/",
            dataType: "json",
            success: function(data) {
                if (data.cleared == 'true'){
                  alert("Cleared suggestions");
                  $('#suggestions_table').empty();
                }
            }
        });
    });

    $('.create-playlist').click(function(){
        $.ajax({
            type: "POST",
            url: "/ajax/create_playlist/",
            dataType: "json",
            data: { "playlist_name": $(".playlist_name").val()},
            success: function(data) {
                alert(data.message)
            }
        });
    });


    $("#search_val").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#suggestions_table tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
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
