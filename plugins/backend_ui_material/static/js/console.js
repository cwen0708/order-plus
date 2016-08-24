// yooliang material backend
// 侑良管理後台
// Version 1.01 (2016/08/21)
// @requires jQuery v2 or later
// Copyright (c) 2016 Qi-Liang Wen 啟良
function json(url,data,successCallback,errorCallback){$.ajax({url:url,type:"POST",dataType:"json",data:data,async:!1,success:function(a){successCallback(a)},error:function(b,c,d){void 0==errorCallback?show_message(d.message):errorCallback(d.message)}})};
function json_async(url,data,successCallback,errorCallback){$.ajax({url:url,type:"POST",cache: false,dataType:"json",data:data,async:1,success:function(a){successCallback(a)},error:function(b,c,d){void 0==errorCallback?show_message(d.message):errorCallback(d.message)}})};
function replaceParam(a,b,c){a=a.replace("#/","");var d="";var m=a.substring(0,a.indexOf("?"));var s=a.substring(a.indexOf("?"),a.length);var j=0;if(a.indexOf("?")>=0){var i=s.indexOf(b+"=");if(i>=0){j=s.indexOf("&",i);if(j>=0){d=s.substring(i+b.length+1,j);s=a.replace(b+"="+d,b+"="+c)}else{d=s.substring(i+b.length+1,s.length);s=a.replace(b+"="+d,b+"="+c)}}else{s=a+"&"+b+"="+c}}else{s=a+"?"+b+"="+c}return s};
function getRandID(a){if(a==undefined){a="rand-id-"}var b="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";for(var i=0;i<5;i++)a+=b.charAt(Math.floor(Math.random()*b.length));return a};

var iframe = {
    "instance": null,
    "history": {},
    "need_focus": false,
    "init": function(selector){
        this.instance = $(selector).get(0);
        $(selector).on("load", function(){
            var url = iframe.getUrl();
            var data = iframe.getState(url);
            if (data) history.replaceState(data, data.text, "#" + data.href);
            iframe.instance.contentWindow.showBackToListButton();
        });
        window.onpopstate = this.popState;
        window["reload_iframe"] = function(){ iframe.reload()};
        window["print_iframe"] = function(){ iframe.print()};
        window["close_msg_nav"] = function(){ $("header").click(); };
        this.history = JSON.parse(localStorage.getItem('iframe.history'));
        if (this.history == null || this.history == "null") this.history = [];
        //TODO 顯示常用的項目
        var sort_list = [];
        var $menu_usually = $("#menu_usually");
        $menu_usually.parent().addClass("hidden");
        $.map(iframe.history, function(n) { if (n.visit > 10){ sort_list.push(n); }});
        sort_list.sort(function(a, b) { return a.visit < b.visit; });
        $.map(sort_list, function(n){
            if ($menu_usually.length < 5){
                $menu_usually.append('<li><a class="waves-attach" href="'+ n.href +'" target="content_iframe">'+ n.text +'</a></li>');
                $menu_usually.parent().removeClass("hidden");
            }
        });
        // ====
        var $linkList = $("a[target=content_iframe]");
        $linkList.click(function(){
            iframe.load($(this).attr("href"), $(this).text());
            event.preventDefault();
        });
        var b = "admin";
        if (window.location.pathname.indexOf("dashboard") >=0){
            b = "dashboard";
        }
        if(window.location.hash) {
            var find_page =false;
            var hash = window.location.hash.replace("#", "");
            $linkList.each(function(){
                if ($(this).attr("href") == hash){
                    find_page = true;
                    $(this).click();
                }
            });
            if (find_page==false){
                var last_page = this.getState(hash);
                if (last_page != null){
                    iframe.load(hash, last_page.text, last_page.referer_page);
                }else{
                    var h = hash.split("/").slice(0, 3).join("/");
                    $linkList.each(function(){
                        if ($(this).attr("href") == h){
                            find_page = true;
                            $(this).click();
                        }
                    });
                }
            }
            if (find_page==false){
                iframe.load("/"+b+"/welcome", "Welcome");
            }
        }else{
            iframe.load("/"+b+"/welcome", "Welcome");
        }
        $(".content").hover(function(){ }, function(){
            setTimeout(function(){
                if (iframe.need_focus == false){
                    $(".iframe_mask").show();
                }
            }, 800);
        });
        $(".iframe_mask").hover(iframe.focus, function(){ iframe.need_focus = false; }).mouseover(iframe.focus).mouseenter(iframe.focus).click(iframe.focus)

    },
    "backToList": function(){
        var data = iframe.getState(location.hash.replace("#", ""));
        iframe.load(data.referer_page);
    },
    "print": function(){
        this.instance.contentWindow.print();
    },
    "focus": function(){
        $(".iframe_mask").hide();
        iframe.need_focus = true;
        iframe.instance.contentWindow.focus();
        var contents = null;
        try{
            contents = $(this.instance).contents();
        }catch(e){
            contents = this.instance.contents();
        }
        contents.find('body').click();
    },
    "removeMask": function(){
        iframe.need_focus = true;
        $(".iframe_mask").hide();
    },
    "reload": function(){
        this.instance.contentWindow.location.reload();
    },
    "saveForm": function(){
        this.instance.contentWindow.save_form();
    },
    "changeLang": function(n){
        this.instance.contentWindow.change_lang(n);
    },
    "getUrl": function(){
        return this.instance.contentWindow.location.pathname;
    },
    "load": function(url, text, referer_page){
        this.pushState(url , text, referer_page);
        var contents = null;
        try{
            contents = $(this.instance).contents();
        }catch(e){
            contents = this.instance.contents();
        }
        contents.find('header').stop().animate({
            top: -70
        }, 250, function(){
            affix(0);
            contents.find('body').addClass("body-hide").html('<div id="onLoad">' +
                '<div class="sk-spinner sk-spinner-chasing-dots">' +
                '<div class="sk-dot1"></div>' +
                '<div class="sk-dot2"></div>' +
                '</div>' +
                '</div>');
        });
        //contents.find("head").append(
        //    $("<link/>", { rel: "stylesheet", href: '/plugins/backend_ui_material/static/css/style.min.css?v=4.1.0', type: "text/css" })
        //);
        $("nav").click();
        this.focus();
        $(this.instance).attr("src", url);
    },
    "getState": function(url) {
        if (url in this.history){
            return iframe.history[url];
        }
        return null;
    },
    "pushState": function(url, text, referer_page){
        var referer_page_data = this.getState(referer_page);
        if (referer_page_data && referer_page_data.referer_page){
            referer_page = referer_page_data.referer_page;
        }
        var history_item = null;
        if (url in this.history){
            history_item = iframe.history[url];
            history_item.last_date = Date.now();
            if (history_item.visit){
                history_item.visit++;
            }else{
                history_item.visit = 1
            }
            localStorage.setItem('iframe.history', JSON.stringify(this.history));
            return false;
        }
        this.history[url] ={
            "href": url,
            "text": text,
            "visit": 1,
            "last_date": Date.now(),
            "referer_page": referer_page
        };
        localStorage.setItem('iframe.history', JSON.stringify(this.history));

    },
    "popState": function(event){
        var s = event.state;
        if (s){
            iframe.load(s.href, s.text, s.is_list);
            window.history.replaceState( s , s.text, "#" + s.href);
        }
    }
};

var message = {
    "list": [],
    "quick_show": function(msg, timeout){
        if (timeout !== undefined){
            swal({
              title: msg,
              html: msg,
              timer: timeout,
              showConfirmButton: false
            });
        }else{
            swal(msg)
        }
    },
    "quick_info": function(msg, sec){
		$('body').snackbar({
            alive: sec,
			content: msg,
			show: function () {
				snackbarText++;
			}
		});
    },
    "showInIframe": function(msg, timeout){
        var current = get_current_tab();
        console.log(current);
        current.iframe.get(0).contentWindow.show_message(msg, timeout);
    },
    "showAll": function(target){
        $(target).find(".alert").each(function(){
            var kind = "info";
            var $alert = $(this);
            if ($alert.hasClass("alert-info")){ kind = "info"; }
            if ($alert.hasClass("alert-warning")){ kind = "warning"; }
            if ($alert.hasClass("alert-success")){ kind = "success"; }
            if ($alert.hasClass("alert-danger")){ kind = "danger"; }
            message.insert(kind, $alert.data("title"), $alert.html(), $alert.data("image"));
        });
    },
    "ui":{
        "show": function(autoHide){
            $(".alert-moment").each(function(){
                var d = $(this).data("create");
                $(this).text(moment(d).fromNow());
            });
            if ($(".msg").length > 25){
                $(".msg").last().remove();
            }
            if (autoHide != undefined && autoHide == true){
                clearTimeout(message.ui.hideTimer);
                message.ui.hideTimerCount = 5;
                message.ui.hideAuto();
            }
        },
        "hideAuto": function(){
            message.ui.hideTimerCount = parseInt(message.ui.hideTimerCount) - 1;
            if (message.ui.hideTimerCount <= 0){
                message.ui.hide();
            }else{
                message.ui.hideTimer = setTimeout(message.ui.hideAuto, 1000);
            }
        },
        "hide": function(){
            $("#message-box").parent("li").removeClass("open");
            message.ui.hideTimerCount = 0;
        }
    },
    "insert": function(kind, title, new_message, image, mini){
        var msg_id = getRandID("message-");
        if (new_message != undefined && new_message != ""){
            message.list.push({"kind": kind, "title": title, "text": new_message, "image": image, "message_id": msg_id, "mini": mini});
        }
        return msg_id;
    },
    "change": function(message_id, kind, title, new_message, image, mini){
        message.list.push({"kind": kind, "title": title, "text": new_message, "image": image, "message_id": message_id, "mini": mini});
    },
    "afterInsert": function(){
        if (message.list.length > 0){
            var p = message.list.pop();
            if (p != undefined && p.text != ""){
                var title = '';
                var tag = '';
                var image = '';
                switch (p.kind) {
                    case "info":
                        tag = '<i class="glyphicon glyphicon-bullhorn"></i>';
                        title = '訊息';
                        break;
                    case "warning":
                        tag = '<i class="glyphicon glyphicon-bell"></i>';
                        title = '注意';
                        break;
                    case "danger":
                        tag = '<i class="glyphicon glyphicon-info-sign"></i>';
                        title = '錯誤';
                        break;
                    case "success":
                        tag = '<i class="glyphicon glyphicon-ok"></i>';
                        title = '成功';
                        break;
                }
                if (p.image != undefined && p.image != ""){
                  tag = '<i class="glyphicon"></i>';
                  image = 'url(' + p.image  + ')';
                }else{
                  image = "none";
                }
                if (p.title != undefined && p.title != ""){ title = p.title; }
                var pid = "#" + p.message_id;
                if ($(pid).length == 0){
                    var insertHtml =
                        '<li class="msg" id="' + p.message_id + '">' +
                            '<div class="alert">' +
                                '<div class="alert-tag" style="background-size: cover;"></div>' +
                                '<span class="alert-moment"></span>' +
                                '<span class="alert-title"></span>' +
                                '<span class="alert-text"></span>' +
                            '</div>' +
                        '</li>';
                    $("#message-box").prepend(insertHtml);
                }
                $(pid).find(".alert-tag").html(tag).removeClass("alert-info alert-warning alert-danger alert-success")
                    .addClass("alert-" + p.kind).css("background-image", image);
                $(pid).find(".alert-moment").data("create", moment().format());
                $(pid).find(".alert-title").text(title);
                $(pid).find(".alert-text").html(p.text);
                $("#message-count").text($("#message-box li").length -1);
                var mini = false;
                if (p.mini != undefined && p.mini == true){ mini = p.mini;}
                if (mini == false){ message.ui.show(true); }
            }
        }
    }
};

var uploader = {
    "addFile": function(file, target_id, callback){
        var message_id = message.insert("info", "準備上傳", "等待中....", undefined, true);
        json_async("/admin/web_file/get.json", null, function(data){
            uploader.upload({
                "message_id": message_id,
                "upload_url": data["url"],
                "file": file,
                "target_id": target_id,
                "callback": callback
            });
        }, function(data){
            message.change(message_id, "danger", "發生錯誤", "無法取得上傳的路徑，請稍候再試一次");
        });
    },
    "upload": function(upload_target){
        var reader = new FileReader();
        reader.reader_info = upload_target;
        reader.readAsDataURL(upload_target.file);
        reader.onload = function(e){
            this.reader_info.image = this.result;
            message.change(this.reader_info.message_id, "info", "正在上傳", "等待中....", this.reader_info.image, true);
            var fd = new FormData();
            var xhr = new XMLHttpRequest();
            xhr.xhr_info = this.reader_info;
            xhr.upload.upload_info = this.reader_info;
            xhr.open('POST', this.reader_info.upload_url);
            xhr.onload = function(data) {
                message.quick_info("上傳完成");
                message.change(this.xhr_info.message_id, "success", "上傳完成", "100 %, 上傳完成", this.xhr_info.image, true);
                if (typeof this.xhr_info.callback === "function"){
                    eval('var a = ' + data.currentTarget.response);
                    this.xhr_info.callback({
                        "response": a,
                        "target_id": this.xhr_info.target_id
                    });
                }
            };
            xhr.onerror = function(e) {
                message.change(this.xhr_info.message_id, "danger", "上傳失敗", "請重整頁面後再試一次", this.xhr_info.image, true);
            };
            xhr.upload.onprogress = function (evt) {
                if (evt.lengthComputable) {
                    var complete = (evt.loaded / evt.total * 100 | 0);
                    if(100==complete){
                        complete=99.9;
                    }
                    message.change(this.upload_info.message_id, "info", "正在上傳", complete + ' %', this.upload_info.image, true);
                }
            };
            fd.append('file_name', this.reader_info.file.name);
            fd.append('file_type', this.reader_info.file.type);
            fd.append('file', this.reader_info.file);
            xhr.send(fd);//開始上傳
        };
        if(/image\/\w+/.test(upload_target.file.type)){
        }
    }
};


$(function(){
    iframe.init("iframe");
    $(document).bind("keydown", function(e) {
        if (e.ctrlKey && e.which == 80) {
            e.preventDefault();
            iframe.print();
            return false;
        }
        if (e.ctrlKey && (e.which == 83)) {
            e.preventDefault();
            iframe.saveForm();
            return false;
        }
        if (e.ctrlKey && e.which == 116 || (e.which || e.keyCode) == 116) {
            e.preventDefault();
            iframe.reload();
            return false;
        }
        if (e.altKey && (e.which >= 49) && (e.which <= 57)) {
            e.preventDefault();
            iframe.changeLang(e.which - 49);
            return false;
        }
    });

    $(".scrollDiv").hover(function(){
        $(this).addClass("on");
        iframe.need_focus = false;
    }, function(){
        $(this).removeClass("on");
    }).mouseover(function(){
        $(this).addClass("on");
    }).mouseover(function(){
        $(this).addClass("on");
    }).mouseleave(function() {
        $(this).removeClass("on");
    });

});
function affix(pos){
    if (pos > 0){
        $("header").addClass("affix");
    }else{
        $("header").removeClass("affix").addClass("affix-top");
    }
}