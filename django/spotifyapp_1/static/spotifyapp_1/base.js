$('ul li a').filter(":contains('Login')").remove();
$('ul li a').filter(":contains('Connect')").remove();
$('ul li a').filter(":contains('Group')").remove();
$('ul li a').filter(":contains('Home')").css('background-color', '#fff');
$('ul li a').filter(":contains('Home')").css('color', '#000');
$(document).ready(function() {

  alert($(location).attr('href'));
  if ($(location).attr('href') == 'file:///C:/Users/shoha/Desktop/Web/templates/dash.html') {
    alert('works');
    $('ul li a').filter(":contains('Login')").remove();
    $('ul li a').filter(":contains('Connect')").remove();
    $('ul li a').filter(":contains('Group')").remove();
    $('ul li a').filter(":contains('Home')").css('background-color', '#fff');
    $('ul li a').filter(":contains('Home')").css('color', '#000');
  }
)};
