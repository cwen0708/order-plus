// yooliang metal backend
// 侑良 Metal 風格後台
// Version 1.00 (2016/1/22)
// @requires jQuery v1.8.2 or later
// Copyright (c) 2016 Qi-Liang Wen 啟良
function json(url,data,successCallback,errorCallback){$.ajax({url:url,type:"POST",cache: false,dataType:"json",data:data,async:!1,success:function(a,m,n){successCallback(a,m,n)},error:function(b,c,d){void 0==errorCallback?toastr.error(d.message):errorCallback(d.message)}})};
function json_as(url,data,successCallback,errorCallback){$.ajax({url:url,type:"POST",cache: false,dataType:"json",contentType: "application/json",data:data,async:1,success:function(a,m,n){successCallback(a,m,n)},error:function(b,c,d){void 0==errorCallback?toastr.error(d.message):errorCallback(d.message)}})};
function ajax(url,data,successCallback,errorCallback){$.ajax({url:url,type:"GET",cache: true,data:data,async:true,success:function(a,m,n){successCallback(a,m,n)},error:function(xhr,ajaxOptions,thrownError){if(errorCallback){errorCallback(xhr.responseText)}else{window.alert(thrownError.message)}}})};
function ajax_post(url,data,successCallback,errorCallback){$.ajax({url:url,type:"POST",cache: true,data:data,async:true,success:function(a,m,n){successCallback(a,m,n)},error:function(xhr,ajaxOptions,thrownError){if(errorCallback){errorCallback(xhr.responseText)}else{window.alert(thrownError.message)}}})};

var material_backend = {
    "store": "",
    "account": "",
    "timezone": 0,
    "debug_item": null,
    "color_list": ["bg-light-blue-a400", "bg-red-a400", "bg-red-a300", "bg-red-900", "bg-red-600", "bg-pink-900", "bg-pink-700", "bg-purple-900", "bg-purple-600",
        "bg-indigo-900", "bg-light-blue-a400", "bg-blue-grey-900", "bg-cyan-900", "bg-teal-900", "bg-green-900", "bg-green-800",
        "bg-lime-900","bg-yellow-900","bg-orange-a400","bg-deep-orange-800","bg-deep-orange-900",
        "bg-brown-900", "bg-brown-800", "bg-grey-900", "bg-grey-800", "bg-grey-600", "bg-orange-800"],
    "change_color": function(color_class_name){
        if (window.localStorage) {
            localStorage.setItem("nav_color", color_class_name);
        }
        var nav = $(".navbar-bg");
        var classList = nav.attr('class').split(/\s+/);
        var old_bg = "";
        $.each(classList, function(index, item) {
            if (item.indexOf('bg-') >= 0) {
                old_bg = item;
            }
        });
        nav.removeClass(old_bg).addClass(color_class_name);
        old_bg = old_bg.replace("bg-", "");
        color_class_name = color_class_name.replace("bg-", "");
        $("." + old_bg).removeClass(old_bg).addClass(color_class_name);
    },
    "next_color": function(){
        var nav = $(".navbar-header");
        var classList = nav.attr('class').split(/\s+/);
        var old_bg = "";
        $.each(classList, function(index, item) {
            if (item.indexOf('bg-') >= 0) {
                old_bg = item;
            }
        });
        $.each(material_backend.color_list, function(index, item) {
            if (item == old_bg) {
                if (index == material_backend.color_list.length-1){
                    material_backend.change_color(material_backend.color_list[0]);
                }else{
                    material_backend.change_color(material_backend.color_list[index+1]);
                }
            }
        });
    },
    "loading_link": null,
    "cache": {
        "set": function(url, data){
            var use_cache = (url.indexOf("cache=local") >=0);
            if (use_cache){
                if (window.localStorage) {
                    var cache_list = localStorage.getItem("cache_list");
                    var cache_list_arr = [url];
                    if (cache_list) {
                        cache_list_arr = cache_list.split("||*||");
                        if (cache_list.indexOf(url) <0){
                            if (cache_list_arr.length > 10 ){
                                localStorage.removeItem(cache_list_arr[0]);
                                cache_list_arr.splice(cache_list_arr,1);
                            }
                            cache_list_arr.push(url);
                        }
                    }
                    localStorage.setItem(url, data);
                    localStorage.setItem("cache_list", cache_list_arr.join("||*||"));
                }
            }
        },
        "get": function(url){
            if (window.localStorage) {
                return localStorage.getItem(url);
            }else{
                return undefined;
            }
        }
    },
    "page": {
        "onClick": function(event){
            var url = $(this).attr("href");
            if (url == "#" || url == undefined) {
                event.stopPropagation();
                event.preventDefault();
                return;
            }
            if (url.indexOf("#") < 0 && url.indexOf("javascript:") < 0) {
                event.stopPropagation();
                event.preventDefault();
                material_backend.page.load($(this).attr("href"), true);
                if ($(this).parent().hasClass("site-menu-item")) {
                    $(".site-menu-item.action").removeClass("action");
                    $(this).parent().addClass("action");
                    $(".navbar-brand-text").html($(this).text());
                }
            }
        },
        "load": function(link, update_history){
            use_cache = (link.indexOf("cache=local") >=0);
            if (link == "/admin/logout"){
                $('#page').html('<div style="text-align: center;margin: 18px;">正在登出...</div>');
                ajax(link, null, function(){
                    location.href = "/admin/login";
                }, function(){
                    location.href = "/admin/login";
                });
                return;
            }
            material_backend.loading_link = link;
            var cache_item = material_backend.cache.get(link);
            if (use_cache && cache_item) {
                $('#page').html(cache_item);
                $.components.init('moment', material_backend.timezone);
            }else{
                $('#page').html('<div style="text-align: center;margin: 18px;">載入中...</div>');
            }
            if (update_history){
                window.history.pushState({url:link,time:new Date().getTime()}, "","/admin#" + link);
            }
            ajax(link, null, material_backend.page.after_load, material_backend.page.after_load);
        },
        "after_load": function(data, status, xhr){
            material_backend.notifications.reset(480);
            toastr.clear();
            var request_url = xhr.getResponseHeader("Request-Url");
            material_backend.cache.set(request_url, data);
            if (request_url != material_backend.loading_link) return false;
            material_backend.loading_link = null;
            $('#page').html(data).find('form').each(function(){
                if ($(this).hasClass("ajax_form") != true) {
                    $(this).submit(material_backend.page.submit);
                    $(this).addClass("ajax_form");
                }
            });
            material_backend.page.checkResponseHeader(xhr);
            if ($(".auto-title").length > 0){
                $(".navbar-brand-text").html($(".auto-title").text());
            }
            $.components.init('moment');
        },
        "checkResponseHeader": function(xhr){
            var request_url = xhr.getResponseHeader("Request-Url");
            var am = xhr.getResponseHeader("Request-Method");
            if (am!="GET"){
                material_backend.notifications.refresh();
            }
            var re_url = xhr.getResponseHeader("Command-Redirect");
            if (re_url){
                return material_backend.page.load(re_url, true);
            }
            $(".site-menu-item a").each(function(){
                if ($(this).attr("href") == request_url){
                    $(".site-menu-item.action").removeClass("action");
                    $(this).parent().addClass("action");
                    if ($(this).parent().parent().hasClass("site-menu-sub")){
                        var id = $(this).parent().parent().parent().attr("id");
                        $('a[data-target="#' + id + '"]').parent().addClass("action");
                    }
                    return false;
                }
            });
        },
        "submit": function(event){
            event.stopPropagation();
            event.preventDefault();
            var data = $(this).serializeArray();
            $("#detailArea input:checkbox").each(function(){
                if (this.checked == false) {
                    console.log($(this).attr("name"));
                    data = data + "&" + $(this).attr("name") + "=";
                }
            });
            var dn = {};
            for (var i =0;i<data.length;i++){
               dn[data[i].name] = data[i].value;
            }
            json_as($(this).attr("action"), JSON.stringify(dn),
                material_backend.page.after_submit, material_backend.page.after_submit);
        },
        "after_submit": function(data, n, x){
            $(".has-error").removeClass("has-error");
            material_backend.notifications.refresh();
            if (data.errors){
                $.each(data.errors, function(error, msg){
                    $("#" + error).next().text(msg.join('<br />')).parent().parent().addClass("has-error");
                });
            }
        },
    },
    "notifications": {
        "list": [],
        "timer": 2,
        "idle": 460,
        "frequency": 60,
        "get_data": function(){
            json_as("/admin/flash_message/get_messages.json", material_backend.notifications.show, material_backend.notifications.show);
        },
        "load": function () {
            material_backend.notifications.timer--;
            if (material_backend.notifications.frequency < 150 && material_backend.notifications.idle % 2)
                material_backend.notifications.frequency++;
            if (material_backend.notifications.timer == 0){
                if (material_backend.notifications.idle > 300){
                    material_backend.notifications.timer = material_backend.notifications.frequency;
                    material_backend.notifications.get_data();
                }else{
                    material_backend.notifications.timer = 5;
                }
            }
            material_backend.notifications.idle--;
            if (material_backend.notifications.idle<0){
                material_backend.notifications.idle = 300;
                material_backend.notifications.get_data();
            }
        },
        "show": function (data) {
            for (var key in data) {
                var item = data[key];
                item.id = key;
                if (item.message === undefined){ continue; }
                var timestamp = moment.unix(key);
                item.created = timestamp.format();
                if (material_backend.notifications.list.indexOf(item.id) < 0) {
                    material_backend.notifications.list.push(item.id);
                    var css_class = "";
                    if (!item.is_read){
                        css_class = "bg-green-600";
                    }else{
                        css_class = "bg-grey-400";
                    }
                    var html = '<a class="list-group-item notifications-item" href="#" ' +
                        'data-sort="' + item.id + '" role="menuitem" id="' + item.id + '">' +
                        '<div class="media">' +
                            '<div class="media-left padding-right-10">' +
                                '<i class="icon zmdi zmdi-comment ' + css_class + ' white icon-circle" aria-hidden="true"></i>' +
                            '</div>' +
                            '<div class="media-body">' +
                                '<h6 class="media-heading moment" data-moment-func="fromNow">' + item.created + '</h6>' +
                                '<div class="media-detail">' + item.message + '</div>' +
                            '</div>' +
                        '</div>' +
                    '</a>';
                    if ($(".notifications-item").length>0){
                        $(".notifications-item").each(function(){
                            if (parseFloat($(this).data("sort")) < parseFloat(item.id)){
                                $(html).insertBefore(this);
                                return false;
                            }
                        });
                    }else{
                        $("#notifications-content").prepend(html);
                    }
                    material_backend.debug_item = item;
                }
            }
            $(".badge.badge-info.up").text($("#notifications-content .bg-green-600").length);
            $.components.init('moment');
        },
        "read": function(id){
            $(id).find(".bg-green-600").removeClass("bg-green-600").addClass("bg-grey-400");
            $(".badge.badge-info.up").text($("#notifications-content .bg-green-600").length);
        },
        "reset": function(idle){
            material_backend.notifications.idle = idle;
            if (material_backend.notifications.frequency > 30){
                material_backend.notifications.frequency -= 10;
            }
            if (material_backend.notifications.timer > 15){
                material_backend.notifications.timer -= 5;
            }
        },
        "refresh": function(){
            material_backend.notifications.timer = 1;
        }
    },
    "interval": function(){
        material_backend.notifications.load();
        $("#process_box").change();
    }
};

(function($){
    var Site = window.Site;
        Site.run();
    $.fn.decimalOnly = function() {
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
            } else
            if (event.keyCode == 190) {  // period
                if ($(this).val().indexOf('.') !== -1) // period already exists
                    event.preventDefault();
                else
                    return;
            } else {
                // Ensure that it is a number and stop the keypress
                if (event.shiftKey || (event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105 )) {
                    event.preventDefault();
                }
            }
        });
    };
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
    };
    window.onpopstate=function()
    {
        var history=window.history.state;
        if (history != null) {
            material_backend.page.load(history.url, false)
        }
    };
    var hash = window.location.hash;
    if (hash){
        hash = hash.replace("#/", "/");
        $(".site-menu a").each(function(){
            if ($(this).attr("href") == hash){
                $(this).parent().addClass("action");
                return false;
            }
        });
        setTimeout(function(){
            material_backend.page.load(hash, false)
        }, 1)
    }

    var console_setting = $(".navbar-bg");
    if (window.localStorage) {
        var nav_color = localStorage.getItem("nav_color");
        if (nav_color){
            material_backend.change_color(nav_color);
        }else{
            localStorage.setItem("nav_color", console_setting.data("color"));
        }
    }
    material_backend.account = console_setting.data("account");
    material_backend.store = console_setting.data("store");
    material_backend.timezone = parseInt(console_setting.data("timezone"));
    $("body").removeClass("hide");
    setTimeout(material_backend.notifications.load, 10);
    setInterval(material_backend.interval, 1000);
})(jQuery);