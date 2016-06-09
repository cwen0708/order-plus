// order msm login
// 簡訊登入
// Version 1.03 (2015/01/03)
// @requires jQuery v1.4.2 or later
// Copyright (c) 2015 Qi-Liang Wen 啟良

(function($){
    $.fn.numericOnly = function() {
        $(this).keydown(function(event) {
             // Allow: backspace, delete, tab, escape, and enter
             if ( event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 || event.keyCode == 13 ||
                  // Allow: Ctrl+A
                 (event.keyCode == 65 && event.ctrlKey === true) ||
                  // Allow: home, end, left, right
                 (event.keyCode >= 35 && event.keyCode <= 39) ||
                 (event.keyCode >= 111 && event.keyCode <= 123)
               ) {
                      // let it happen, don't do anything
                      return;
             } else {
                 // Ensure that it is a number and stop the keypress
                 if (event.shiftKey || (event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105 )) {
                     event.preventDefault();
                 }
             }
         });
     }
})(jQuery);
var code_300_counter = null;
jQuery(document).ready(function($) {
    $( "#code" ).keypress(function( event ) {
        if ( event.which == 13 ) {
            event.preventDefault();
            $(this).next().click();
        }
    });
    $("#login").click(function(){
        var data = $("form").serialize();
        $.ajax({
            type: "post",
            url: "/admin/login.json",
            data: data,
            async: true,
            dataType: "json",
            jsonpCallback:"callback"
        }).done(function(data) {
            if (data.is_login == "true"){
                $("#msg_info").html("登入成功，請稍候...").slideDown(function(){
                    setTimeout(function(){
                        $("#msg_info").slideUp();
                    }, 3000);
                    location.href = "/admin";
                });
            }else{
                $("#msg_error").html("登入失敗，帳號密碼有誤").slideDown(function(){
                    setTimeout(function(){
                        $("#msg_error").slideUp();
                    }, 3000);
                });
            }
        }).error(function(data){
            $("#msg_error").html("登入時發生錯誤了，請稍候再試").slideDown(function(){
                setTimeout(function(){
                    $("#msg_error").slideUp();
                }, 3000);
            });
        });
    });
    $("#mobile").numericOnly();
});
