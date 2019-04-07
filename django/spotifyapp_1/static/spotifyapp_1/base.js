$(document).ready(function() {
  alert($(location).attr('href'));
  if ($(location).attr('href') == 'https://cs411-spotify.herokuapp.com/dash/') {
    alert('works');
    $('ul li a').filter(":contains('Login')").remove();
    $('ul li a').filter(":contains('Connect')").remove();
    $('ul li a').filter(":contains('Group')").remove();
    $('ul li a').filter(":contains('Home')").css('background-color', '#fff');
    $('ul li a').filter(":contains('Home')").css('color', '#000');
  }
});
