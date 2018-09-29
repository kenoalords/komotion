import $ from "jquery";
import slick from "slick-carousel";

(function(){

    if ( $('.carousel').length > 0 ){
        $('.carousel').slick({
            autoplay: true,
            infinite: true,
            dots: true,
            fade: true,
        })
    }

    if ( $('.is-carousel').length > 0 ){
        $('.is-carousel').slick({
            autoplay: true,
            infinite: true,
            dots: true,
            slidesToShow: 4,
            slidesToScroll: 4,
        })
    }

})()
