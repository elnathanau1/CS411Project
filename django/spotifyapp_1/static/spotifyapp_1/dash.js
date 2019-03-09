$(document).ready(function() {
  $.ajax({
    type: "GET"
    url: "/ajax/top_artists/"
    success: function(data) {
      // jQuery selector
      $('#top_artist_table').append('<tr><th>'+data[i]+'</th></tr>')
    }
  })

});
