$(document).ready(function() {
  $.ajax({
    type: "GET"
    url: "/ajax/top_artists/"
    success: function(data) {
      $('table').append('<tr><th>'+data[i]+'</th></tr>')
    }
  })

});
