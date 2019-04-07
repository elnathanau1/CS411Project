$(document).ready(function() {
    if ($(location).attr('href') == 'https://cs411-spotify.herokuapp.com/dash/') {
      $('ul li a').filter(":contains('Login')").remove();
      $('ul li a').filter(":contains('Connect')").remove();
      $('ul li a').filter(":contains('Group')").remove();
      $('ul li a').filter(":contains('Home')").css('background-color', '#fff');
      $('ul li a').filter(":contains('Home')").css('color', '#000');
    }

    if ($(location).attr('href') == 'https://cs411-spotify.herokuapp.com/about_us/') {
      $('ul li a').filter(":contains('Log out')").remove();
      $('ul li a').filter(":contains('Connect')").remove();
      $('ul li a').filter(":contains('Group')").remove();
      $('ul li a').filter(":contains('About us')").remove();
      $('ul li a').filter(":contains('Home')").remove();
    }

    if ($(location).attr('href') == 'https://cs411-spotify.herokuapp.com/login/') {
      $('ul li a').filter(":contains('Log out')").remove();
      $('ul li a').filter(":contains('Home')").remove();
      $('ul li a').filter(":contains('Group')").remove();
      $('ul li a').filter(":contains('Connect')").remove();
      $('ul li a').filter(":contains('Login')").remove();
    }
});
