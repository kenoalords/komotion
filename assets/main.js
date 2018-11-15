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

    $('body').on('click', '#add-course-form', function(e){
        e.preventDefault();
        var formTemplate = $('#empty-course-item-form').html(),
            formContainer = $('#file-forms'),
            formCount = formContainer.children().length,
            compiledFormTemplate = formTemplate.replace(/__prefix__/g, formCount);
        formContainer.append(compiledFormTemplate);
        $('#id_form-TOTAL_FORMS').attr('value', formCount+1);
    });

    var rank = 0, duration = 0;
    $('.subscription-form').on('change', function(e){
        var $this = $(e.target);
        if (  $this.hasClass('rank') ){
            $('.rank').each(function(index, el){
                $(el).parents('label').removeClass('is-checked');
                $(el).parents('.pricing-plan').removeClass('is-active');
            });
            $this.parents('label').addClass('is-checked');
            $this.parents('.pricing-plan').addClass('is-active');
            rank = $this.val();
        }
        if ( $this.hasClass('duration') ){
            duration = $this.val();
        }
        
        if ( parseInt(rank) > 0 && parseInt(duration) > 0 ){
            $('#submit-subscription').removeAttr('disabled');
        } else {
            $('#submit-subscription').attr('disabled', 'disabled');
        }
    })

})()
