;$(function()
{
    'use strict';
    var sidebar =$('#sidebar'),
        sidebar_trigger = $('#sidebar-trigger'),
        backbutton=$('.back-to-top'),
        main_page=$('.main-page');
    function backback()
    {
        $('html,body').animate({
            scrollTop:0
        },800)
    }
//    sidecont.animate({'left':-250},{duration:500,queue:false});
    function hidebutton()
    {
        if($(window).scrollTop() > $(window).height()/2)
            backbutton.fadeIn();
        else
            backbutton.fadeOut();
    }
    function showSideBar()
    {

        sidebar.animate({'left':0},{duration:500,queue:false});
        /*main_page.css('margin-left',sidebar.width());*/
        main_page.animate({'margin-left':sidebar.width()},{duration:300,queue:false})

    }
    function hideSideBar()
    {
        sidebar.animate({'left':-sidebar.width()},{duration:500,queue:false});
        main_page.animate({'margin-left':0},{duration:500,queue:false});
    }
    function showhideSideBar()
    {
			
            if(sidebar.css('left')=='0px'){
				
                hideSideBar();}
            else{
				
                showSideBar();}
    }
    $(function(){
        
            $(function(){setTimeout(hideSideBar,600)});
            sidebar_trigger.on('click',showhideSideBar);
            backbutton.on('click',backback);
            $(window).on('scroll',hidebutton);
            $(window).trigger('scroll');
        
    })
        
    
    /*sidebar_trigger.on('click',showSideBar)*/
})