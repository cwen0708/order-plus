// yooliang general function
// 侑良通用函式
// Version 1.03 (08/18/2012)
// @requires jQuery v1.4.2 or later
// Copyright (c) 2012 Qi-Liang Wen 啟良
function json(url,data,successCallback,errorCallback){$.ajax({url:url,type:"POST",cache: false,dataType:"json",data:data,async:!1,success:function(a){successCallback(a)},error:function(b,c,d){void 0==errorCallback?show_tom_message(d.message):errorCallback(d.message)}})};
function json_as(url,data,successCallback,errorCallback){$.ajax({url:url,type:"POST",cache: false,dataType:"json",data:data,async:1,success:function(a){successCallback(a)},error:function(b,c,d){void 0==errorCallback?show_tom_message(d.message):errorCallback(d.message)}})};
function ajax(url,data,successCallback,errorCallback){$.ajax({url:url,type:"GET",cache: true,data:data,async:true,success:function(responseText){successCallback(responseText)},error:function(xhr,ajaxOptions,thrownError){if(errorCallback){errorCallback(xhr.responseText)}else{window.alert(thrownError.message)}}})};
function ajax_post(url,data,successCallback,errorCallback){$.ajax({url:url,type:"POST",cache: true,data:data,async:true,success:function(responseText){successCallback(responseText)},error:function(xhr,ajaxOptions,thrownError){if(errorCallback){errorCallback(xhr.responseText)}else{window.alert(thrownError.message)}}})};

var drap_style_timer = null;
function onDragStart(evt){
    evt.preventDefault();
    evt.stopPropagation();
    $("html").addClass("dropping");
    $(".img_selector_div, .imgs_selector_div").parent().parent().addClass("dropping-box");
}
function onDragEnd(evt){
    evt.preventDefault();
    evt.stopPropagation();
    drap_style_timer = setTimeout(function(){
        $("html").removeClass("dropping");
        $(".img_selector_div, .imgs_selector_div").parent().parent().removeClass("dropping-box");
        }, 1000);
}
function onDragOver(evt) {
    evt.preventDefault();
    evt.stopPropagation();
    clearTimeout(drap_style_timer);
    $("html").addClass("dropping");
    $(".img_selector_div, .imgs_selector_div").parent().parent().addClass("dropping-box");
}
function onDrop(evt) {
    var files = evt.dataTransfer.files;
    evt.preventDefault();
    $("html").removeClass("dropping");
    $(".img_selector_div, .imgs_selector_div").parent().parent().removeClass("dropping-box");
    if (files.length > 10){
        backend.message.insert("danger", "錯誤", "一次可上傳 10個文件", undefined);
        return;
    }
    for (var i=0; i<files.length; i++) {
        console.log(evt.target);
        backend.uploader.addFile(files[i], evt.target);
    }
}

var backend = {
    "dom": {
        "menu": null,
        "menu_firstLevel": null,
        "menu_secondLevel": null,
        "list": null,
        "detail": null,
        "search_input": null,
        "search_button": null,
        "message": null,
        "message_button": null,
        "message_temp_html": null
    },
    "menu": {
        "init": null,
        "firstLoaded": false,
        "firstLevel": {
            "click": null
        },
        "secondLevel": {
            "click": null
        }
    },
    "list": {
        "load": null,
        "afterLoad": null,
        "reload": null,
        "lastUrl": "",
        "isLock": false
    },
    "detail": {
        "load": null,
        "afterLoad": null,
        "afterSubmit": null,
        "lastUrl": "",
        "show": null,
        "hide": null,
        "isShow": false,
        "isLock": false
    },
    "grid": {
        "selectRecord": null,
        "unselectRecord": null,
        "editRecord": null,
        "lastSelectRecord": null,
        "lastTarget": null
    },
    "method": {
        "makeAjaxForm": null,
        "reSize": null,
        "deleteRecordCheck": null,
        "search": null
    },
    "uploader": {
        "addFile": null,
        "start": null
    },
    "message": {
        "ui": {
            "show": null,
            "hide": null,
            "hideTimer": null,
            "hideTimerCount": 5
        },
        "list": [],
        "change": null,
        "insert": null,
        "afterInsert": null,
        "showAll": null
    },
    "selector": {
        "image": {
            "last_target": null,
            "last_target_editor": null,
            "options": {
                success: function (files) {
                    backend.selector.image.selected(files[0].link);
                },
                cancel: function () {
                },
                linkType: "direct",
                multiselect: false,
                extensions: ['.jpg', '.gif', '.jpeg', '.png']
            },
            "server_selected": null,
            "selected": null,
        },
        "images": {
            "last_target": null,
            "options": {
                success: function (files) {
                    var list = [];
                    for (var i=0; i<files.length;i++){
                        list.push(files[i].link);
                    }
                    backend.selector.images.selected(list);
                },
                cancel: function () {
                },
                linkType: "direct",
                multiselect: true,
                extensions: ['.jpg', '.gif', '.jpeg', '.png']
            }
        }

    }
};
Object.defineProperty(backend.message.list, "push", {
    configurable: false,
    enumerable: false, // hide from for...in
    writable: false,
    value: function () {
        for (var i = 0, n = this.length, l = arguments.length; i < l; i++, n++) {
            this[n] = arguments[i];
            backend.message.afterInsert(); // assign/raise your event
        }
        return n;
    }
});


// 處理選單事件
backend.menu.init = function(){
    $(window).resize(function(){
        $(".sidebar .main-nav").height($(window).height() - 100);
    }).resize();
    backend.detail.isShow = false;
    $(backend.dom.menu_firstLevel).click(backend.menu.firstLevel.click);
    $(backend.dom.menu_secondLevel).click(backend.menu.secondLevel.click);
    $(backend.dom.menu_secondLevelP).click(function (event) {
        $(backend.dom.menu_secondLevel).click(backend.menu.secondLevel.click);
        $(this).find("a").first().click();
    });
    $(backend.dom.menu_firstLevel).first().click();
    setTimeout(function(){
        $(backend.dom.search_button).click(function(){
            event.stopPropagation();
            event.preventDefault();
            backend.method.search($(backend.dom.search_input).val());
        });
        $(backend.dom.search_input).keyup(function(event){
            if (event.which == 13) {
                event.preventDefault();
                $(backend.dom.search_button).click();
            }
        });
        $(".header .search").slideDown();
        $(window).click(function(event){
            if ($(event.target).parents(backend.dom.message).length == 0 &&
                $(event.target).parents(backend.dom.message_button).length == 0 &&
                $(event.target).hasClass("message-box-button") == false &&
                $(event.target).hasClass("show-message") == false &&
                $(event.target).hasClass("alert-close") == false
            ){
                backend.message.ui.hide();
            }
        });

        // 伺服器圖片挑選功能
        $( "body" ).append(backend.dom.message_temp_html).on("click", ".select-one .images-selector-box", function() {
            if ($('.select-one .images-selector-box.selected') != $(this)){
                $('.select-one .images-selector-box.selected').removeClass("selected");
            }
            $(this).addClass("selected");
        }).on("click", ".select-many .images-selector-box", function() {
            if ($(this).hasClass("selected")){
                $(this).removeClass("selected");
            }else{
                $(this).addClass("selected");
            }
        }).on("dblclick", ".img_selector_item", function(){
            var p = $(this).parent();
            if (p.hasClass("imgs_selector_div")){
                $(this).remove();
                var t = [];
                p.find(".img_selector_item").each(function(){
                    t.push($(this).data("link"));
                });
                backend.selector.images.selected(t, p.find("textarea").attr("id"), true);
            }
            if (p.hasClass("img_selector_div")){
                backend.selector.image.selected("", p.find("input").attr("id"));
            }
        }).on("click", backend.dom.message_button, function(){
            backend.message.ui.show();
        });

    }, 300);
};
// 第一層選單按下時
backend.menu.firstLevel.click = function (event) {
    event.stopPropagation();
    event.preventDefault();
    var checkElement = $(this).next();
    $('.main-nav li').removeClass('active');
    $(this).closest('li').addClass('active');
    if ((checkElement.is('ul')) && (checkElement.is(':visible'))) {
        $(this).closest('li').removeClass('active').removeClass('is_open');
        checkElement.slideUp('normal');
    }
    if ((checkElement.is('ul')) && (!checkElement.is(':visible'))) {
        $(this).closest('li').addClass('is_open');
        $('.main-nav ul ul:visible').slideUp('normal').parent().removeClass('is_open');
        checkElement.slideDown('normal');
    }
    if (checkElement.is('ul')) {
        if (backend.menu.firstLoaded == false){
            $(backend.dom.menu_secondLevel).first().click();
            backend.menu.firstLoaded = true;
        }
        return false;
    } else {
        var url = $(this).attr("href");
        if (url !== "#"){
            $('.main-nav ul > li > ul > li.sub_active').removeClass('sub_active');
            backend.list.load(url);
            backend.menu.firstLoaded = true;
        }else{
            if (backend.menu.firstLoaded == false){
                $(backend.dom.menu_secondLevel).first().click();
                backend.menu.firstLoaded = true;
            }
        }
    }
};
// 第二層選單按下時
backend.menu.secondLevel.click = function (event) {
    event.stopPropagation();
    event.preventDefault();
    var url = $(this).attr("href");
    if (url !== "#"){
        $('.main-nav ul > li > ul > li.sub_active').removeClass('sub_active');
        $(this).parent().addClass('sub_active');
        if ($(this).parents("active").length == 0){
            $('.main-nav li').removeClass('active');
            $(this).parents("ul").parents("li").addClass("active");
        }
        backend.list.load(url);
    }
};

backend.grid.selectRecord= function(event){
    if (w2ui[event.target]) {
        var selected_list = w2ui[event.target].getSelection();
        if (event.all !== undefined && event.all === true){
            for (var i=0;i<w2ui[event.target].records.length;i++){
                selected_list.push(parseInt(w2ui[event.target].records[i]["recid"]));
            }
        }else{
            if (event.recid !== undefined){
                selected_list.push(parseInt(event.recid));
            }
        }
    }
};
backend.grid.unselectRecord = function(event){
    if (event !== undefined && event !== null){
        if (w2ui[event.target]) {
            var selected_list = w2ui[event.target].getSelection();
            var new_list = [];
            for (var i=0;i<selected_list.length;i++){
                if (parseInt(selected_list[i]) !== parseInt(event.recid)){
                    new_list.push(selected_list[i]);
                }
            }
        }
    }else{
        backend.detail.hide();
    }
};
backend.grid.editRecord = function(event){
    if (w2ui[event.target]) {
        var selected_list = w2ui[event.target].getSelection();
        if (event.all !== undefined && event.all === true){
            for (var i=0;i<w2ui[event.target].records.length;i++){
                selected_list.push(parseInt(w2ui[event.target].records[i]["recid"]));
            }
        }else{
            if (event.recid !== undefined){
                selected_list.push(parseInt(event.recid));
                backend.grid.showRecord(event.target, event.recid)
            }
        }
    }
};
selectRecord = backend.grid.selectRecord;
unselectRecord = backend.grid.unselectRecord;
editRecord = backend.grid.editRecord;

backend.grid.showRecord = function(target, recid){
    for (var i=0;i< w2ui[target].records.length;i++){
        if (w2ui[target].records[i]["recid"] == recid){
            var url = w2ui[target].records[i]["edit_url"];
            backend.grid.lastSelectRecord = url;
            backend.detail.load(url);
        }
    }
};


backend.method.makeAjaxForm = function(target){
    var $target = $(target);
    $target.find('form').each(function(){
        if ($(this).hasClass("ajax_form") == false) {
            $(this).submit(function(event){
                event.stopPropagation();
                event.preventDefault();
                var data = $(this).serialize();
                $("#detailArea input:checkbox").each(function(){
                    if (this.checked == false) {
                        console.log($(this).attr("name"));
                        data = data + "&" + $(this).attr("name") + "=";
                    }
                });
                ajax_post($(this).attr("action"), data, function(page){
                    backend.detail.afterSubmit(page);
                }, function(page){
                    backend.detail.afterSubmit(page);
                });
            });

            $(this).addClass("ajax_form");
        }
    });
};

// 列表頁載入
backend.list.load = function(url, is_reload){
    if (backend.list.isLock == true){
        return;
    }
    backend.list.isLock = true;
    var rnid = backend.method.getRndID("load-");
    url = backend.method.replaceParam(url, "rnid", rnid);
    if (is_reload == undefined || is_reload == false){
        backend.detail.hide();
        $(backend.dom.list).html('<div class="records"><h1>載入中…</h1></div>').addClass("has-list");
        ajax(url, null, backend.list.afterLoad, backend.list.afterLoad);
    }else{
        ajax(url, null, function(page) {
            backend.list.afterLoad(page);
        }, function(page){
            backend.list.afterLoad(page);
        });
    }
    backend.list.lastUrl = url;
};
// 列表頁載入後
backend.list.afterLoad = function(page){
    $(backend.dom.list).html(page);
    backend.message.showAll(backend.dom.list);
    var list = [];
    var n = 0;
    var has_list = false;
    $(backend.dom.list).find(".records-list li").each(function(){
        list.push({
            "recid": n,
            "title": $(this).data("title"),
            "edit_url": $(this).data("edit-url"),
            "delete_url": $(this).data("delete-url"),
            "sort_up_url": $(this).data("sort-up-url"),
            "sort_down_url": $(this).data("sort-down-url"),
            "sort_in_category": $(this).data("sort-in-category"),
            "desc": $(this).data("desc"),
            "html": $(this).html()
        });
        n++;
    });
    if ($(backend.dom.list).find(".records-list").length > 0){has_list = true;}
    if (has_list){
        $(backend.dom.list).addClass("has-list");
        backend.grid.lastTarget = backend.method.getRndID("grid-");
        $(backend.dom.list).find('.records-list').w2grid({
            name: backend.grid.lastTarget,
            header: 'List of Names',
            show: {
                columnHeaders: false,
                selectColumn: true
            },
            sortData: [{ field: 'recid', direction: 'ASC' }],
            records: list,
            columns: [
                { field: 'list-item', caption: '', size: '100%', render: function (record, index, column_index) {
                    return  record.html;
                }},
                { field: 'list-item-2', caption: '', size: '100px', render: function (record, index, column_index) {
                    if (record.sort_up_url != undefined){
                        var cursor = $("#mainArea .records").data("cursor");
                        if (cursor == undefined || cursor == "None"){
                            cursor = "False"
                        }
                        record.sort_up_url = backend.method.replaceParam(record.sort_up_url, "cursor", cursor);
                        record.sort_down_url = backend.method.replaceParam(record.sort_down_url, "cursor", cursor);
                        if (record.sort_in_category != undefined && record.sort_in_category != ""){
                            record.sort_up_url = backend.method.replaceParam(record.sort_up_url, "category", record.sort_in_category);
                            record.sort_down_url = backend.method.replaceParam(record.sort_down_url, "category", record.sort_in_category);
                        }
                        return '<button class="btn btn-sort-up" onclick="backend.method.sortRecord(\'' + record.sort_up_url + '\', true)">▲</button>' +
                            '<button class="btn btn-sort-down" onclick="backend.method.sortRecord(\'' + record.sort_down_url + '\', true)">▼</button>';
                    }
                }},
                { field: 'list-item-2', caption: '', size: '90px', render: function (record, index, column_index) {
                    return '<button class="btn btn-default" onclick="backend.detail.load(\'' + record.edit_url + '\')">編輯</button>';
                }},
                { field: 'list-item-2', caption: '', size: '90px', render: function (record, index, column_index) {
                    if (record.delete_url != undefined){
                        return '<button class="btn btn-default" onclick="backend.method.deleteRecordCheck(\'' + record.delete_url + '\')">刪除</button>';
                    }
                }},
            ],
            onUnselect: unselectRecord,
            onDblClick: editRecord,
            onSelect: selectRecord
        });
        var records = w2ui[backend.grid.lastTarget].records;
        for (var i=0;i< records.length;i++){
            if (records[i]["edit_url"] == backend.detail.lastUrl){
                var recid = records[i]["recid"];
                w2ui[backend.grid.lastTarget].select(recid);
            }
        }
    }else{
        $(backend.dom.list).removeClass("has-list");
    }

    backend.method.makeAjaxForm(backend.dom.list);
    var h = 0;
    $(backend.dom.list).find(".operation").each(function(){ h = h + 1;});
    if (h == 0){
        $("#mainArea .records-list").addClass("not-operation");
    }
    $(".btn-add-record").click(function(){
        event.stopPropagation();
        event.preventDefault();
        backend.detail.load($(this).attr("href"));
    });
    $(".pager a").click(function(){
        event.stopPropagation();
        event.preventDefault();
        backend.list.load($(this).attr("href"), true);
    });
    if (backend.detail.isShow == true){
        backend.detail.show();
    }
    backend.list.isLock = false;
    backend.method.reSize(100);
    backend.method.reSize(200);
    backend.method.reSize(300);
};
// 列表頁重新載入
backend.list.reload = function(){
    backend.list.load(backend.list.lastUrl, true);
};

// 詳細頁載入
backend.detail.load = function(url){
    if (backend.detail.isLock == true){
        return;
    }
    if (backend.detail.isShow == false){
        backend.detail.show();
    }
    backend.detail.isLock = true;
    $(backend.dom.detail).html('<section class="record"><h1> 載入中… </h1></div>');
    ajax(url, null, backend.detail.afterLoad, backend.detail.afterLoad);
    backend.detail.lastUrl = url;
};
// 詳細頁載入後
backend.detail.afterLoad = function(page){
    $(backend.dom.detail).html(page);
    backend.method.makeAjaxForm(backend.dom.detail);
    $(backend.dom.detail).find(".btn-submit").click(function(){
        event.stopPropagation();
        event.preventDefault();
        var _form = $(this).parents("form");
        _form.find(".field-type-rich-text-field").each(function(){
            var id = $(this).attr("id");
            if (tinyMCE.get(id)){
                $(this).val(tinyMCE.get(id).getContent());
            }
            $(this).change();
        });
        _form.submit();
    });
    $(backend.dom.detail).find(".img_selector_div, .imgs_selector_div").each(function(){
       var copy = $(this).prev();
       $(this).prev().remove();
       $(copy).insertAfter($(this).children().first());
    });
    $(backend.dom.detail).find(".btn-cancel").click(function(){
        event.stopPropagation();
        event.preventDefault();
        backend.detail.hide();
    });
    $('input.field-type-date-field').w2field('date',  { format: 'yyyy-mm-dd' });
    $('input.field-type-image-property-field').parents(".form-item").addClass("form-item-with-border");
    $('textarea.field-type-images-property-field').parents(".form-item").addClass("form-item-with-border");
    $(".btn-image-open-dropbox").click(function(){
        backend.selector.image.last_target = $(this).data("target");
        Dropbox.choose(backend.selector.image.options);
    });
    $(".btn-images-open-dropbox").click(function(){
        backend.selector.images.last_target = $(this).data("target");
        Dropbox.choose(backend.selector.images.options);
    });
    $(".btn-image-open-server").click(function(){
        backend.selector.image.last_target = $(this).data("target");
        ajax('/admin/web_file/images_list', null, function(page){
            w2popup.open({
                title     : '選擇圖片',
                body      : '<div class="select-one">' + page + '</div>',
                buttons   : '<button class="btn" onclick="backend.selector.image.server_selected(); w2popup.close();">確定</button> '+
                            '<button class="btn" onclick="w2popup.close();">取消</button>',
                width     : $("body").width() * 0.65,
                height    : $("body").height() * 0.65,
                overflow  : 'hidden',
                color     : '#333',
                speed     : '0.3',
                opacity   : '0.8',
                modal     : true,
                showClose : true
            });
        });
    });
    $(".btn-images-open-server").click(function(){
        backend.selector.images.last_target = $(this).data("target");
        ajax('/admin/web_file/images_list', null, function(page){
            w2popup.open({
                title     : '選擇圖片',
                body      : '<div class="select-many">' + page + '</div>',
                buttons   : '<button class="btn" onclick="backend.selector.images.server_selected(); w2popup.close();">確定</button> '+
                            '<button class="btn" onclick="w2popup.close();">取消</button>',
                width     : $("body").width() * 0.65,
                height    : $("body").height() * 0.65,
                overflow  : 'hidden',
                color     : '#333',
                speed     : '0.3',
                opacity   : '0.8',
                modal     :  true,
                showClose : true
            });
        });
    });
    $(".btn-image-open-google-picker").click(function(){
        backend.selector.image.last_target = $(this).data("target");
        //TODO 讓使用者挑選 google 相冊 單一圖片
    });
    $(".btn-images-open-google-picker").click(function(){
        backend.selector.images.last_target = $(this).data("target");
        //TODO 讓使用者挑選 google 相冊
    });
    $('input.field-type-color-property-field').w2field('color');
    backend.detail.isLock = false;
    backend.message.showAll(backend.dom.detail);
    tinyMCE.editors=[];
    $(".field-type-rich-text-field").each(function() {
        var label_name = $(this).prev().text();
        $(this).prev().remove();
        var id = $(this).attr("id");
        if (id == undefined){ id = $(this).attr("name"); $(this).attr("id", id); }
        if (id) {
            var ed = tinyMCE.createEditor(id, {
                theme : 'modern',
                content_css : ["/plugins/backend_ui_saimiri/static/TinyMCE/4.2.5/skins/lightgray/content.min.css"],
                height: 400,
                plugins: [
                    "link image media code table preview hr anchor pagebreak textcolor fullscreen colorpicker "
                ],
                toolbar: "editor_title | undo redo | styleselect | alignleft aligncenter alignright forecolor backcolor bold italic | link upload_image image media | code custom_fullscreen",
                statusbar: false,
                menubar: false,
                setup : function(ed) {
                    ed.addButton('editor_title', {
                        title : '此為編輯器所對應的欄位名稱',
                        text : label_name
                    });
                    ed.addButton('upload_image', {
                        title : '插入圖片',
                        image : '/plugins/backend_ui_saimiri/static/TinyMCE/4.2.5/themes/upload_image.png',
                        onclick : function() {
                            // Add you own code to execute something on click
                            backend.selector.image.last_target = ed.id + "#editor";
                            backend.selector.image.last_target_editor = ed;
                            ajax('/admin/web_file/images_list', null, function(page){
                                w2popup.open({
                                    title     : '選擇圖片',
                                    body      : '<div class="select-one">' + page + '</div>',
                                    buttons   : '<button class="btn" onclick="backend.selector.image.server_selected(); w2popup.close();">確定</button> '+
                                                '<button class="btn" onclick="w2popup.close();">取消</button>',
                                    width     : $("body").width() * 0.65,
                                    height    : $("body").height() * 0.65,
                                    overflow  : 'hidden',
                                    color     : '#333',
                                    speed     : '0.3',
                                    opacity   : '0.8',
                                    modal     : true,
                                    showClose : true
                                });
                            });
                        }
                    });

                    ed.addButton('custom_fullscreen', {
                        title: '全螢幕',
                        text: '全螢幕',
                        onclick : function() {
                            debugger;
                            if ($(".nav-settings").is(":visible") == true){
                                $(".nav-settings").hide();
                                $("#message-box-button").hide();
                                backend.message.ui.hide();
                            }else{
                                $(".nav-settings").show();
                                $("#message-box-button").show();
                            }
                            ed.execCommand('mceFullScreen');
                        }
                    });
                    ed.on('init', function (e) {
                        setTimeout('$(backend.dom.detail).scrollTop(0);', 10);
                        setTimeout('$(backend.dom.detail).scrollTop(0);', 20);
                        setTimeout('$(backend.dom.detail).scrollTop(0);', 300);
                    })
                },
                convert_urls:false,
                relative_urls:false,
                remove_script_host:false
            });
            ed.render();
        }
    });
};
// 詳細頁資料送出後
backend.detail.afterSubmit = function(page){
    backend.list.reload();
    var $p = $('<div>' + page + '</div>');
    var $p_item = $p.find(".form-item");
    var n = 0;
    for (var i=0;i<$p_item.length;i++){
        console.log(i)
    }
    $(backend.dom.detail + " .form-item").each(function(){
        if ($p_item.eq(n).hasClass("has-error")){
            $(this).find(".help-block").text($p_item.eq(n).find(".help-block").text());
            $(this).addClass("has-error");
        }else{
            $(this).find(".help-block").text("");
            $(this).removeClass("has-error");
        }
        n++;
    });
    $p.find(".alert").each(function(){
        var kind = "info";
        var $alert = $(this);
        if ($alert.hasClass("alert-info")){ kind = "info"; }
        if ($alert.hasClass("alert-warning")){ kind = "warning"; }
        if ($alert.hasClass("alert-success")){ kind = "success"; }
        if ($alert.hasClass("alert-danger")){ kind = "danger"; }
        backend.message.insert(kind, $alert.data("title"), $alert.html(), $alert.data("image"));
    });
//    backend.detail.afterLoad(page);
};
// 詳細頁顯示
backend.detail.show = function(){
    if (backend.detail.isShow == false){
        backend.detail.isShow = true;
        w2ui['layout2'].show('right');
    }
    $(".btn-add-record").removeClass("detailAreaIsOpen").addClass("detailAreaIsOpen");
    $("#mainArea .pager").removeClass("detailAreaIsOpen").addClass("detailAreaIsOpen");
};
// 詳細頁隱藏
backend.detail.hide = function(){
    backend.detail.isShow = false;
    w2ui['layout2'].hide('right');
    $(".btn-add-record").removeClass("detailAreaIsOpen");
    $("#mainArea .pager").removeClass("detailAreaIsOpen");
};

backend.method.sortRecord = function(url){
    ajax(url, null, function(){
        backend.list.reload();
    }, function(){
        backend.list.reload();
    });
};

backend.method.deleteRecordCheck = function(url){
    w2confirm({
        "msg": "是否要刪除此項目",
        "title": "刪除?",
        "yes_text": "是的, 刪除它",
        "no_text": "取消"
    }).yes(function(){
        if (url.replace("/delete", "") == backend.detail.lastUrl.replace("/edit", "")){ backend.detail.hide(); }
        ajax(url, null, function(){
            backend.list.reload();
            backend.message.insert("success", "刪除成功", "此項目已經被刪除了");
        }, function(){
            backend.list.reload();
            backend.message.insert("danger", "刪除失敗", "請確認要刪除的目標是否還存在，或稍後再試一次");
        });
    });
};
backend.method.reSize = function(s){
    setTimeout(function(){
        var w = $("#layout_layout2_panel_main #mainArea").width() + 250;
        $(".btn-add-record").css("left", w - 90);
        $(".detailAreaIsOpen.btn-add-record").css("left", w - 53);
        var pw = $("#mainArea .pager").width();
        $("#mainArea .pager").css("left", w - 100 - pw);
        $("#mainArea .detailAreaIsOpen.pager").css("left", w - 68 - pw);
    }, s);
};
backend.method.search = function(keyword){
    if (keyword != undefined && keyword != ""){
        var url = backend.method.replaceParam(backend.list.lastUrl, "query", keyword);
        url = backend.method.replaceParam(url, "cursor", "");
        url = url.replace("?cursor=none", "?");
        url = url.replace("&cursor=none", "");
        backend.list.load(url);
    }
    if (keyword == ""){
        var url = backend.method.replaceParam(backend.list.lastUrl, "query", "");
        backend.list.load(url);
    }
};
backend.message.showAll = function(target){
    $(target).find(".alert").each(function(){
        var kind = "info";
        var $alert = $(this);
        if ($alert.hasClass("alert-info")){ kind = "info"; }
        if ($alert.hasClass("alert-warning")){ kind = "warning"; }
        if ($alert.hasClass("alert-success")){ kind = "success"; }
        if ($alert.hasClass("alert-danger")){ kind = "danger"; }
        backend.message.insert(kind, $alert.data("title"), $alert.html(), $alert.data("image"));
    });
};
backend.message.insert = function(kind, title, new_message, image, mini){
    var msg_id = backend.method.getRndID("message-");
    if (new_message != undefined && new_message != ""){
        backend.message.list.push({"kind": kind, "title": title, "text": new_message, "image": image, "message_id": msg_id, "mini": mini});
    }
    return msg_id;
};
backend.message.change = function(message_id, kind, title, new_message, image, mini){
    backend.message.list.push({"kind": kind, "title": title, "text": new_message, "image": image, "message_id": message_id, "mini": mini});
};
backend.message.afterInsert = function(){
    if (backend.message.list.length > 0){
        var p = backend.message.list.pop();
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
                    '<li class="msg not-ready" style="display:none;" id="' + p.message_id + '">' +
                        '<div class="alert">' +
                            '<div class="alert-tag" style="background-size: cover;"></div>' +
                            '<button type="button" class="alert-close close" data-dismiss="alert">×</button>' +
                            '<span class="alert-moment"></span>' +
                            '<span class="alert-title"></span>' +
                            '<span class="alert-text"></span>' +
                        '</div>' +
                    '</li>';
                $(backend.dom.message).find("ul").prepend(insertHtml);
            }
            $(pid).find(".alert-tag").html(tag).removeClass("alert-info alert-warning alert-danger alert-success")
                .addClass("alert-" + p.kind).css("background-image", image);
            $(pid).find(".alert-moment").data("create", moment().format());
            $(pid).find(".alert-title").text(title);
            $(pid).find(".alert-text").html(p.text);

            var mini = false;
            if (p.mini != undefined && p.mini == true){ mini = p.mini;}
            if (mini == false){ backend.message.ui.show(true); }
        }
    }
};
backend.message.ui.hideAuto = function(){
    backend.message.ui.hideTimerCount = parseInt(backend.message.ui.hideTimerCount) - 1;
    if (backend.message.ui.hideTimerCount <= 0){
        backend.message.ui.hide();
    }else{
        backend.message.ui.hideTimer = setTimeout(backend.message.ui.hideAuto, 1000);
    }
};
backend.message.ui.show = function(autoHide){
    $(".alert-moment").each(function(){
        var d = $(this).data("create");
        $(this).text(moment(d).fromNow());
    });
    if($(backend.dom.message).hasClass("is_show")){
        $("#message-box .msg.not-ready").fadeIn(function () {
            $(this).removeClass("not-ready")
        });
    }else{
        $(backend.dom.message).show(function () {
            $("#message-box .msg.not-ready").fadeIn(function () {
                $(this).removeClass("not-ready")
            });
            $(backend.dom.message).addClass("is_show");
        });
    }
    if ($(".msg").length > 25){
        $(".msg").last().remove();
    }
    if (autoHide != undefined && autoHide == true){
        clearTimeout(backend.message.ui.hideTimer);
        backend.message.ui.hideTimerCount = 5;
        backend.message.ui.hideAuto();
    }
};
backend.message.ui.hide = function(){
    $(backend.dom.message).fadeOut();
    $(backend.dom.message).removeClass("is_show");
    backend.message.ui.hideTimerCount = 0;
};

backend.selector.image.server_selected = function(){
    if ($('.select-one .images-selector-box.selected').length > 0){
        var link = $('.select-one .images-selector-box.selected').first().data("link");
        backend.selector.image.selected(link);
    }
};
backend.selector.images.server_selected = function(){
    var list = [];
    $('.select-many .images-selector-box.selected').each(function(){
        list.push($(this).data("link"));
    });
    backend.selector.images.selected(list);
};
backend.selector.image.selected = function(link, target){
    if (target == undefined) {
        target = backend.selector.image.last_target;
    }
    if (target.indexOf("#editor") > 0){
        backend.selector.image.last_target_editor.selection.setContent('<img src="' + link + '" />');
    }else{
        $("#" + target).val(link );
        if (link == ""){
            $("#img-" + target).css("background-image", "none").addClass("img_selector_item_none");
        }else{
            $("#img-" + target).css("background-image", "url(" + link + ")").removeClass("img_selector_item_none");
        }
    }
};
backend.selector.images.selected = function(list, target, replace){
    if (target == undefined){
        target = backend.selector.images.last_target;
    }
    if (replace == true){
        $("#" + target).val("");
        $("#" + target).parent().find(".img_selector_item").remove();
    }
    for (var i=0; i<list.length;i++){
        var v = $("#" + target).val() + ";" + list[i];
        $("#" + target).val(v).parent().append('<div class="img_selector_item" data-link="' + list[i] + '" style="background-image: url(' + list[i] + ')"></div>');
    }
};

backend.uploader.start = function(target){
    if(/image\/\w+/.test(target.file.type)){
        var reader = new FileReader();
        reader.info = target;
        reader.readAsDataURL(target.file);
        reader.onload = function(e){
            this.info.image = this.result;
            backend.message.change(this.info.message_id, "info", "正在上傳", "等待中....", this.info.image);
            var fd = new FormData();
            var xhr = new XMLHttpRequest();
            xhr.xhrinfo = this.info;
            xhr.upload.xhrinfo = this.info;
            xhr.open('POST', this.info.upload_url);
            xhr.onload = function(data) {
                backend.message.change(this.xhrinfo.message_id, "success", "上傳完成", "100 %, 上傳完成", this.xhrinfo.image);
                var tres  = data.currentTarget.response;
                if (this.xhrinfo.target != undefined){
                    var t = this.xhrinfo.target;
                    for (var i=0; i<10;i++) {
                        if (t.className.indexOf("img_selector_div") >= 0){
                            console.log(t.firstChild.id);
                            backend.selector.image.selected(tres, t.firstChild.id);
                            i = 11;
                        }
                        if (t.className.indexOf("imgs_selector_div") >= 0){
                            console.log(t.firstChild.id);
                            backend.selector.images.selected([tres], t.firstChild.id);
                            i = 11;
                        }
                        if (t.className.indexOf("mce-content-body") >= 0){
                            var editor_id = $(t).data("id");
                            tinyMCE.get(editor_id).execCommand('mceInsertContent', false, '<img src="' + tres + '" />');
                            i = 11;
                        }

                        console.log(t);
                        t = t.parentElement;
                        if (t == null){
                            return;
                        }

                    }
                }
            };
            xhr.onerror = function(e) {
                backend.message.change(this.xhrinfo.message_id, "danger", "上傳失敗", "請重整頁面後再試一次", this.xhrinfo.image);
            };
            xhr.upload.onprogress = function (evt) {
                if (evt.lengthComputable) {
                    var complete = (evt.loaded / evt.total * 100 | 0);
                    if(100==complete){
                        complete=99.9;
                    }
                    backend.message.change(this.xhrinfo.message_id, "info", "正在上傳", complete + ' %', this.xhrinfo.image);
                }
            };
            fd.append('file', this.info.file);
            xhr.send(fd);//開始上傳
        };
    }
};
backend.uploader.addFile = function(file, target){
    var file_info = {
        "message_id": backend.message.insert("info", "準備上傳", "等待中...."),
        "upload_url": null,
        "file": file,
        "target": target
    };
    ajax("/admin/web_file/get.json", null, function(data){
        file_info.upload_url = data["url"];
        backend.uploader.start(file_info);
    }, function(data){
        backend.message.change(file_info.message_id, "danger", "發生錯誤", "無法取得上傳的路徑，請稍候再試一次");
    });
};
var ready = false;
$(function () {
    console.log("%c%s","color: red; background: yellow; font-size: 24px;","\u8b66\u544a\uff01");
    console.log("%c%s","color: black; font-size: 18px;","\u4f7f\u7528\u6b64\u63a7\u5236\u53f0\u53ef\u80fd\u6703\u8b93\u653b\u64ca\u8005\u6709\u6a5f\u6703\u5229\u7528\u540d\u70ba Self-XSS \u7684\u653b\u64ca\u65b9\u5f0f\u5192\u7528\u60a8\u7684\u8eab\u5206\uff0c\u7136\u5f8c\u7aca\u53d6\u60a8\u7684\u8cc7\u8a0a\u3002\n\u8acb\u52ff\u8f38\u5165\u6216\u8cbc\u4e0a\u4f86\u6b77\u4e0d\u660e\u7684\u7a0b\u5f0f\u78bc\u3002");
    var pstyle = 'background-color: #fff; border: 0px solid #dfdfdf; padding: 0px;';
    var header_height = $(".layout-header").height();
    backend.dom.message_temp_html = $(".layout-message-area").html();
    $(".layout-header").remove();
    $().w2layout({
        "name": 'layout2',
        "panels": [
            { type: 'top', size: header_height, resizable: false, style: 'background-color: #ddd;border: 0px; padding: 0px', content: $('.layout-search-area').html(), overflow: 'hidden' },
            { type: 'main', minSize: 550, style: 'background-color: #ffffff; border: 0px solid #dfdfdf; padding: 0px; border-right: solid 0px #ddd;', content: $('.layout-main-area').html() },
            { type: 'right', size: '50%', resizable: true, hidden: true, style: pstyle, content: $('.layout-side-area').html()}
        ],
        "onRender": function(event) {
            backend.menu.init();
        },
        "onResize": function(event) {
            backend.method.reSize(100);
            backend.method.reSize(200);
            backend.method.reSize(300);
        },
        "padding": 0
    });
    $('body').w2layout({
        "name": 'layout',
        "panels": [
            { type: 'left', size: 250, resizable: false, style:  'border: 0px; padding: 0px;', content: $('.layout-menu-area').html(), overflow: 'hidden' },
            { type: 'main', style: 'background-color: white;', overflow: 'hidden'},
            { type: 'preview', size: '50%', resizable: true, hidden: true, style: pstyle, content: 'preview' },
            { type: 'bottom', size: 50, resizable: true, hidden: true, style: pstyle, content: 'bottom' }
        ],
        "padding": 0
    });
    w2ui['layout'].content('main', w2ui['layout2']);
    // 預載，確保第一次載入編輯器時，不會失敗
    tinyMCE.init({
        "content_css": ["/plugins/backend_ui_saimiri/static/TinyMCE/4.2.5/skins/lightgray/content.min.css"],
        "height": 400,
        "statusbar": false,
        "menubar": false,
        "convert_urls": false,
        "relative_urls": false,
        "remove_script_host": false
    });
    backend.dom.list = "#layout_layout2_panel_main #mainArea";
    backend.dom.detail = "#layout_layout2_panel_right #detailArea";
    backend.dom.menu = "#layout_layout_panel_left .main-nav";
    backend.dom.menu_firstLevel = ".main-nav > ul > li > a";
    backend.dom.menu_secondLevel = ".main-nav ul > li > ul > li > a";
    backend.dom.menu_secondLevelP = ".main-nav ul > li > ul > li";
    backend.dom.message = "#message-box";
    backend.dom.message_button = "#message-box-button";
    backend.dom.search_input = ".search input";
    backend.dom.search_button = ".search a";
    $( document ).on( "click", ".alert-close", function() {
        $(this).parent().parent().remove();
    });
});

backend.method.replaceParam=function(a,b,c){a=a.replace("#/","");var d="";var m=a.substring(0,a.indexOf("?"));var s=a.substring(a.indexOf("?"),a.length);var j=0;if(a.indexOf("?")>=0){var i=s.indexOf(b+"=");if(i>=0){j=s.indexOf("&",i);if(j>=0){d=s.substring(i+b.length+1,j);s=a.replace(b+"="+d,b+"="+c)}else{d=s.substring(i+b.length+1,s.length);s=a.replace(b+"="+d,b+"="+c)}}else{s=a+"&"+b+"="+c}}else{s=a+"?"+b+"="+c}return s};
backend.method.getRndID=function(a){if(a==undefined){a="grid-"}var b="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";for(var i=0;i<5;i++)a+=b.charAt(Math.floor(Math.random()*b.length));backend.grid.lastTarget=a;return a};