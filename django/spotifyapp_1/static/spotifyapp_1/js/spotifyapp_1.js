$(document).ready(function() {
    // AJAX GET
    $('.get-more').click(function(){
        console.log("sigh")
        $.ajax({
            type: "GET",
            url: "/ajax/more/",
            success: function(data) {
            for(i = 0; i < data.length; i++){
                $('ul').append('<li>'+data[i]+'</li>');
            }
        }
        });

    });
});
