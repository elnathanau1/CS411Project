if ($(location).attr('href') == 'https://cs411-spotify.herokuapp.com/dash/') {
  $('ul li a').filter(":contains('Login')").remove();
  $('ul li a').filter(":contains('Home')").css('background-color', '#fff');
  $('ul li a').filter(":contains('Home')").css('color', '#000');
}

if ($(location).attr('href') == 'https://cs411-spotify.herokuapp.com/about_us/') {
  // $('ul li a').filter(":contains('Log out')").remove();
  $('ul li a').filter(":contains('About us')").remove();
}

if ($(location).attr('href') == 'https://cs411-spotify.herokuapp.com/login/') {
    $('ul li a').filter(":contains('Log in')").remove();
    $('ul li a').filter(":contains('Log out')").remove();
    $('ul li a').filter(":contains('Dash')").remove();
}

if ($(location).attr('href') == 'https://cs411-spotify.herokuapp.com/connect/') {
    $('ul li a').filter(":contains('Log in')").remove();
    $('ul li a').filter(":contains('Log out')").remove();
    $('ul li a').filter(":contains('Dash')").remove();
}
