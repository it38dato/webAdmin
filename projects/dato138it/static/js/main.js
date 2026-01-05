$(function() {
    /* Fixed Header */
    var header = $("#header"),
        pageH = $("#page__fixed").innerHeight(),
        scrollOffset = $(window).scrollTop();
    checkScroll(scrollOffset);
    $(window).on("scroll", function() {
        scrollOffset = $(this).scrollTop();
        checkScroll(scrollOffset);
    });
    function checkScroll(scrollOffset) {
        if( scrollOffset >= pageH ) {
            header.addClass("fixed");
        } else {
            header.removeClass("fixed");
        }
    }
    /* Smooth scroll */
    $("[data-scroll]").on("click", function(event) {
        event.preventDefault();
        var $this = $(this),
            blockId = $this.data('scroll'),
            blockOffset = $(blockId).offset().top;
        $("#nav a").removeClass("active");
        $this.addClass("active");
        $("html, body").animate({
            scrollTop:  blockOffset
        }, 500);
    });
    /* Filter CARDS  */
    let filter = $("[data-filter]");
    filter.on("click", function(event) {
        event.preventDefault();
        let cat = $(this).data('filter');
        if(cat == 'all') {
            $("[data-cat]").removeClass("cards__hide");
        } else {
            $("[data-cat]").each(function() {
                let workCat = $(this).data('cat');
                if(workCat != cat) {
                    $(this).addClass('cards__hide');
                } else {
                    $(this).removeClass('cards__hide');
                }
            });
        }
    });
    /* Modal */
    const modalCall = $("[data-modal]");
    const modalClose = $("[data-close]");
    modalCall.on("click", function(event) {
        event.preventDefault();
        let $this = $(this);
        let modalId = $this.data('modal');
        $(modalId).addClass('show');
        $("body").addClass('modal__noscroll');
        setTimeout(function() {
            $(modalId).find(".modal__dialog").css({
                transform: "scale(1)"
            });
        }, 200);
        worksSlider.slick('setPosition');
    });
    modalClose.on("click", function(event) {
        event.preventDefault();
        let $this = $(this);
        let modalParent = $this.parents('.modal');
        modalParent.find(".modal__dialog").css({
            transform: "scale(0)"
        });
        setTimeout(function() {
            modalParent.removeClass('show');
            $("body").removeClass('modal__noscroll');
        }, 200);
    });
    $(".modal").on("click", function(event) {
        let $this = $(this);
        $this.find(".modal__dialog").css({
            transform: "scale(0)"
        });
        setTimeout(function() {
            $this.removeClass('show');
            $("body").removeClass('modal__noscroll');
        }, 200);
    });
    $(".modal__dialog").on("click", function(event) {
        event.stopPropagation();
    });
});
/*Hide card*/
var ns6=document.getElementById&&!document.all?1:0
var head="display:''"
var folder=''
function card__hidden(curobj){
    folder=ns6?curobj.nextSibling.nextSibling.style:document.all[curobj.sourceIndex+1].style
    if (folder.display=="none")
        folder.display=""
    else
        folder.display="none"
}