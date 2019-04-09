$(document).ready(function() {

    //loaded immediately after page is done loading
    $.ajax({
        type: "GET",
        url: "/ajax/get_songs/",
        success: function(data) {
            console.log(data);
            for(i = 0; i < data.songs.length; i++){
            // jQuery selector
              $('#songs_table').append('<tr><td>'+data.songs[i]+'</td></tr>')

            }
        }
    });

    // AJAX POST
    $('.add-song').click(function(){
        console.log("clicked")
        $.ajax({
            type: "POST",
            url: "/ajax/add_song/",
            dataType: "json",
            data: { "new_song_id": $(".new_song_id").val()},
            success: function(data) {
                alert(data.message)
            }
        });
    });

    $("#search_val").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#songs_table tr").filter(function() {
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
