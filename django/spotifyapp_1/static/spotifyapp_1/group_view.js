// Reorganizing and styling navigation bar
$('ul li a').filter(":contains('Login')").remove();
$('ul li a').filter(":contains('Connect')").remove();
$('ul li a').filter(":contains('Group')").css('background-color', '#c5c6c7');
$('ul li a').filter(":contains('Group')").css('color', 'blue');
$('ul li a').filter(":contains('Group')").text('Group');

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

    // AJAX POST
    $('.change-group-name').click(function(){
        console.log("clicked")
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
