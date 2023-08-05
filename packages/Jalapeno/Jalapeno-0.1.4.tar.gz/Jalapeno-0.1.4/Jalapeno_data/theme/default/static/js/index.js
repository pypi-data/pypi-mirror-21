;$(function()
{
    'use strict';/*严格模式*/
  
    var logo =$(".logo"),
        mask =$(".mask"),
        heading=$('.heading');

    
    function run(){
        window.location='posts.html';
    }
    
    $(function(){mask.fadeIn(4000)}) 
    $(function(){logo.fadeIn(2000)})
    $(function(){heading.delay(3000).fadeIn(1000)})
    $(function(){setTimeout(run,5000)})
    
    
})