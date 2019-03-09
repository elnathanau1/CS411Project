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

});
