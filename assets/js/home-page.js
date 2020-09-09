// Course Card Slider Functionality 
$(document).ready(function () {
    $(".owl-carousel").owlCarousel();
});
$('.owl-carousel').owlCarousel({
    loop: true,
    margin: 20,
    nav: true,
    navText: [
        "<i class='fas fa-arrow-circle-left'></i>",
        "<i class='fas fa-arrow-circle-right'></i>"
    ],
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 3
        },
        1000: {
            items: 4
        }
    }
});



