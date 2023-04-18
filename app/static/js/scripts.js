$(function(){

$('.fancybox').fancybox({
    padding: 0,
    helpers: {
    overlay: {
            locked: false
        }
    },
    lang : 'ru',
    i18n : {
        'ru' : {
            CLOSE : 'Закрыть',
            NEXT: "Далее",
            PREV: "Назад",
            ERROR: "Запрошенные данные не могут быть загружены. <br/> Повторите попытку позже.",
            PLAY_START: "Начать слайд-шоу",
            PLAY_STOP: "Завершить слайд-шоу",
            FULL_SCREEN: "На весь экран",
            THUMBS: "Миниатюры",
            DOWNLOAD: "Скачать",
            SHARE: "Поделиться",
            ZOOM: "Увеличить"
        }
    }
});



// validation
$('.rf').each(function(){
    var item = $(this),
    btn = item.find('.button');
    
    function checkInput(){
        item.find('select.required').each(function(){
            if($(this).val() == '0'){
                $(this).parents('.form-group').addClass('error');
                $(this).parents('.form-group').find('.error-message').show();
            } else {
                $(this).parents('.form-group').removeClass('error');
            }
        });                
        
        item.find('input[type=text].required').each(function(){
            if($(this).val() != ''){
                $(this).removeClass('error');
            } else {
                $(this).addClass('error');
                $(this).parent('.form-group').find('.error-message').show();
            }
        });
        
        item.find('input[type=email]').each(function(){
            var regexp = /^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$/i;
            var $this = $(this);
            if($this.hasClass('required')){
                if (regexp.test($this.val())) {
                    $this.removeClass('error');
                } else {
                    $this.addClass('error');
                    $(this).parent('.form-group').find('.error-message').show();
                }
            } else{
                if($this.val() != ''){
                    if (regexp.test($this.val())) {
                        $this.removeClass('error');
                    }else {
                        $this.addClass('error');
                        $(this).parent('.form-group').find('.error-message').show();
                    }
                } else{
                    $this.removeClass('error');
                }
            }                    
        });                
        
    }

    btn.click(function(){
        checkInput();
        var sizeEmpty = item.find('.error:visible').length;
        if(sizeEmpty > 0){
            return false;
        } else {                    
            item.submit();
            $.fancybox.close();
        }
    });
});

// end validation     



$('.fancybox').fancybox({
    padding: 0,
    helpers: {
    overlay: {
            locked: false
        }
    },
    lang : 'ru',
    i18n : {
        'ru' : {
            CLOSE : 'Закрыть',
            NEXT: "Далее",
            PREV: "Назад",
            ERROR: "Запрошенные данные не могут быть загружены. <br/> Повторите попытку позже.",
            PLAY_START: "Начать слайд-шоу",
            PLAY_STOP: "Завершить слайд-шоу",
            FULL_SCREEN: "На весь экран",
            THUMBS: "Миниатюры",
            DOWNLOAD: "Скачать",
            SHARE: "Поделиться",
            ZOOM: "Увеличить"
        }
    }
});

$('.select-styler').styler({
    selectSearch: false
});


$('#fileInputWrap input[type="file"]').on('change', function(){
    let input = $(this);
    let label = $(this).parent().find('label');
    if(this.files != null){
        let upload_files = this.files;
        let reader = new FileReader();
        reader.readAsDataURL(upload_files.item(0));
        reader.onload = function (e) {
            var item = `
            <div class="item-img">
                <div class="delete">
                    <svg width="38" height="46" viewBox="0 0 38 46" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M11.4366 5.34813C11.4366 2.67237 13.2038 0.503662 15.3841 0.503662H23.2793C25.4597 0.503662 27.2269 2.67237 27.2269 5.34813V6.96296H36.4379C37.1643 6.96296 37.7538 7.6864 37.7538 8.57778C37.7538 9.46917 37.1643 10.1926 36.4379 10.1926H33.8062V37.6446C33.8062 42.1031 30.86 45.7187 27.2269 45.7187H11.4366C7.80346 45.7187 4.85725 42.1031 4.85725 37.6446V10.1926H2.22553C1.49917 10.1926 0.909668 9.46917 0.909668 8.57778C0.909668 7.6864 1.49917 6.96296 2.22553 6.96296H11.4366V5.34813ZM14.0683 6.96296H24.5952V5.34813C24.5952 4.45675 24.0057 3.73331 23.2793 3.73331H15.3841C14.6578 3.73331 14.0683 4.45675 14.0683 5.34813V6.96296ZM7.48897 10.1926V37.6446C7.48897 40.3204 9.25617 42.4891 11.4366 42.4891H27.2269C29.4073 42.4891 31.1745 40.3204 31.1745 37.6446V10.1926H7.48897ZM19.3317 15.0371C20.0581 15.0371 20.6476 15.7605 20.6476 16.6519V36.0298C20.6476 36.9212 20.0581 37.6446 19.3317 37.6446C18.6054 37.6446 18.0159 36.9212 18.0159 36.0298V16.6519C18.0159 15.7605 18.6054 15.0371 19.3317 15.0371Z" fill="black"/>
                    </svg>
                </div>
                <a href="`  + e.target.result +  `" class="absolute fancybox" data-fancybox="portfolio"></a>
                <img src="`  + e.target.result +  `" alt="">
            </div>
            `;
            label.append(item);
            $(".delete").on('click', function(){
                $(this).parent(".item-img").remove();
                input.val('');
            });
        };
    }
});
$('#fileInputImgVideo input[type="file"]').on('change', function(){
    let input = $(this);
    let label = $(this).parent().find('label');
    if(this.files != null){
        let reader = new FileReader();
        reader.readAsDataURL(this.files.item(0));
        reader.onload = function (e) {
            if(input[0].files[0].type.substring(0,5) == 'video'){
                var item = `
                <div class="item-img">
                    <div class="delete">
                        <svg width="38" height="46" viewBox="0 0 38 46" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M11.4366 5.34813C11.4366 2.67237 13.2038 0.503662 15.3841 0.503662H23.2793C25.4597 0.503662 27.2269 2.67237 27.2269 5.34813V6.96296H36.4379C37.1643 6.96296 37.7538 7.6864 37.7538 8.57778C37.7538 9.46917 37.1643 10.1926 36.4379 10.1926H33.8062V37.6446C33.8062 42.1031 30.86 45.7187 27.2269 45.7187H11.4366C7.80346 45.7187 4.85725 42.1031 4.85725 37.6446V10.1926H2.22553C1.49917 10.1926 0.909668 9.46917 0.909668 8.57778C0.909668 7.6864 1.49917 6.96296 2.22553 6.96296H11.4366V5.34813ZM14.0683 6.96296H24.5952V5.34813C24.5952 4.45675 24.0057 3.73331 23.2793 3.73331H15.3841C14.6578 3.73331 14.0683 4.45675 14.0683 5.34813V6.96296ZM7.48897 10.1926V37.6446C7.48897 40.3204 9.25617 42.4891 11.4366 42.4891H27.2269C29.4073 42.4891 31.1745 40.3204 31.1745 37.6446V10.1926H7.48897ZM19.3317 15.0371C20.0581 15.0371 20.6476 15.7605 20.6476 16.6519V36.0298C20.6476 36.9212 20.0581 37.6446 19.3317 37.6446C18.6054 37.6446 18.0159 36.9212 18.0159 36.0298V16.6519C18.0159 15.7605 18.6054 15.0371 19.3317 15.0371Z" fill="black"/>
                        </svg>
                    </div>
                    <video src="`  + e.target.result +  `" width="100%" height="auto" controls></video>
                </div>
                `;
            }
            else{
                var item = `
                <div class="item-img">
                    <div class="delete">
                        <svg width="38" height="46" viewBox="0 0 38 46" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M11.4366 5.34813C11.4366 2.67237 13.2038 0.503662 15.3841 0.503662H23.2793C25.4597 0.503662 27.2269 2.67237 27.2269 5.34813V6.96296H36.4379C37.1643 6.96296 37.7538 7.6864 37.7538 8.57778C37.7538 9.46917 37.1643 10.1926 36.4379 10.1926H33.8062V37.6446C33.8062 42.1031 30.86 45.7187 27.2269 45.7187H11.4366C7.80346 45.7187 4.85725 42.1031 4.85725 37.6446V10.1926H2.22553C1.49917 10.1926 0.909668 9.46917 0.909668 8.57778C0.909668 7.6864 1.49917 6.96296 2.22553 6.96296H11.4366V5.34813ZM14.0683 6.96296H24.5952V5.34813C24.5952 4.45675 24.0057 3.73331 23.2793 3.73331H15.3841C14.6578 3.73331 14.0683 4.45675 14.0683 5.34813V6.96296ZM7.48897 10.1926V37.6446C7.48897 40.3204 9.25617 42.4891 11.4366 42.4891H27.2269C29.4073 42.4891 31.1745 40.3204 31.1745 37.6446V10.1926H7.48897ZM19.3317 15.0371C20.0581 15.0371 20.6476 15.7605 20.6476 16.6519V36.0298C20.6476 36.9212 20.0581 37.6446 19.3317 37.6446C18.6054 37.6446 18.0159 36.9212 18.0159 36.0298V16.6519C18.0159 15.7605 18.6054 15.0371 19.3317 15.0371Z" fill="black"/>
                        </svg>
                    </div>
                    <a href="`  + e.target.result +  `" class="absolute fancybox" data-fancybox="portfolio"></a>
                    <img src="`  + e.target.result +  `" alt="">
                </div>
                `;
            }
            label.append(item);
            $(".delete").on('click', function(){
                $(this).parent(".item-img").remove();
                input.val('');
            });
        };
    }
});

    var d = new Date();
    var month = d.getMonth()+1;
    var day = d.getDate();
    var output =  (day<10 ? '0' : '') + day + '.' +
        (month<10 ? '0' : '') + month + '.' +
        d.getFullYear();


    $('.today').val(output);


}); // end document ready;
