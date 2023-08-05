;$(function()
{
    'use strict';
    var sidebar =$('#sidebar'),
        sidebar_trigger = $('#sidebar-trigger'),
        main_page=$('#main-page');
    function backback()
    {
        $('html,body').animate({
            scrollTop:0
        },800)
    }
    
    function hidebutton()
    {
        if($(window).scrollTop() > $(window).height()/2)
            backbutton.fadeIn();
        else
            backbutton.fadeOut();
    }
    function showSideBar()
    {
        console.log('aaaa');
        sidebar.css('left',0);
        /*main_page.css('margin-left',sidebar.width());*/
        main_page.animate({'margin-left':sidebar.width()})
        sidebar_trigger.text("➤");
    }
    function hideSideBar()
    {
        sidebar.css('left',-sidebar.width());
        main_page.animate({'margin-left':0});
        
    }
    function showhideSideBar()
    {
            if(sidebar.css('left')=='0px')
                hideSideBar();
            else  
                showSideBar();
    }
    $(function(){
        if($(window).width()>1024){
            
            sidebar_trigger.on('click',showhideSideBar);
            backbutton.on('click',backback);
            sidebar_item.on('click',hideSideBar);
            $(window).on('scroll',hidebutton);
            $(window).trigger('scroll');
        }
    })
        
    
    /*sidebar_trigger.on('click',showSideBar)*/
})
// ;$(function()
// {
//     'use strict';
//     var sidebar =$('#sidebar'),
//         sidebar_trigger = $('#sidebar-trigger'),
       
//         main_page=$('#main-page');


//     function showSideBar()
//     {
        
//         $('#sidebar').css('left',0);
//         /*main_page.css('margin-left',sidebar.width());*/
//         $('#main-page').animate({'margin-left':$('#sidebar').width()})
//         $('#sidebar-trigger').text("#");
//     }
//     function hideSideBar()
//     {
//         $('#sidebar').css('left',-$('#sidebar').width());
//         $('#main-page').animate({'margin-left':0});
//         $('#sidebar-trigger').text("☰");
//     }
//     function showhideSideBar()
//     {
//             if($('#sidebar').css('left')=='0px')
//                 hideSideBar();
//             else  
//                 showSideBar();
//     }
//     // $(function(){
//         alert('aaa');
//             // sidebar_trigger.on('click',showhideSideBar);
//             $('#sidebar-trigger').on('click',function(){
//               alert('aaa');
//               // showhideSideBar();
//             });

//     // })
        
    
//     /*sidebar_trigger.on('click',showSideBar)*/
// })

