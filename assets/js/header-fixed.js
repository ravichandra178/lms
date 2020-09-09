
var desktopMenuPosition = $('#desktopMenu').offset();
console.log(desktopMenuPosition);
$(window).scroll(function () {
  if ($(window).scrollTop() > desktopMenuPosition.top) {
    $('#desktopMenu').css('position', 'fixed').css('top', '0').css('background-color', 'white').css('width', '100%');
    // $("#pageLanding").css('padding-top','100px');
    $('#imgMenu').css('background-color', 'white');
  } else {
    $('#desktopMenu').css('position', 'static');
    // $("#pageLanding").css('padding-top','0px');
  }
});

var mobileMenuPosition = $('#mobileMenu').offset();
$(window).scroll(function () {
  if ($(window).scrollTop() > mobileMenuPosition.top) {
    $('#mobileMenu').css('position', 'fixed').css('top', '0').css('background-color', 'white').css('width', '100%');
    $('#mobileMenu .navbar-collapse').css("top","70px");
    // $("#pageLanding").css('padding-top','100px');
  } else {
    $('#mobileMenu').css('position', 'static');
    $('#mobileMenu .navbar-collapse').css("top","120px");
    // $("#pageLanding").css('padding-top','0px');
  }
});
