
function json(url,data,successCallback,errorCallback)       {$.ajax({url:url,type:"POST",dataType:"json",cache: false,data:data,async:!1,success:function(a){successCallback(a)},error:function(b,c,d){void 0==errorCallback?show_message(b.responseJSON.error):errorCallback(b.responseJSON)}})};
function json_async(url,data,successCallback,errorCallback) {$.ajax({url:url,type:"POST",dataType:"json",cache: false,data:data,async:1 ,success:function(a){successCallback(a)},error:function(b,c,d){void 0==errorCallback?show_message(b.responseJSON.error):errorCallback(b.responseJSON)}})};
function ajax_post(url,data,successCallback,errorCallback)  {$.ajax({url:url,type:"POST",cache: true,data:data,async:true,success:function(responseText){successCallback(responseText)},error:function(xhr,ajaxOptions,thrownError){if(errorCallback){errorCallback(xhr.responseText)}else{window.alert(thrownError.message)}}})};
function getRandID(a){if(a==undefined){a="rand-id-"}var b="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";for(var i=0;i<5;i++)a+=b.charAt(Math.floor(Math.random()*b.length));return a};
var save_with_exit = false;

var backend = parent;
var backToList = backend.iframe.backToList;

function showBackToListButton(){
    $(".backToList").show();
}

function show_message(msg, timeout){
    backend.message.quick_show(msg, timeout);
}
var start_filepicker = backend.start_filepicker;

function parent_is_ready(){
    show_message = backend.message.quick_show;
    start_filepicker = backend.start_filepicker;
}
if (backend.js_is_ready && backend.js_is_ready == true){
    var show_message = backend.message.quick_show;
    var start_filepicker = backend.start_filepicker;
}

    window.onpopstate = function(event){
        console.log("iframe event" + event);
    };
var pageDOD = {
    "visual_timer": 3,
    "init": function(){
        if ($(".img_selector_div, .imgs_selector_div, .field-type-rich-text-field").length == 0){
            $("#dropping").addClass("no_target");
        }
    },
    "onDragStart": function(evt){
        evt.preventDefault();
        evt.stopPropagation();
        $("html").addClass("dropping");
        $(".img_selector_div, .imgs_selector_div").parent().parent().addClass("dropping-box");
    },
    "onDragEnd": function (evt){
        evt.preventDefault();
        evt.stopPropagation();
        pageDOD.visual_timer=0;
        setTimeout(pageDOD.removeVisualClass, 1000);
    },
    "onDragOver": function (evt){
        evt.preventDefault();
        evt.stopPropagation();
        pageDOD.visual_timer=3;
        $("html").addClass("dropping");
        $(".img_selector_div, .imgs_selector_div").parent().parent().addClass("dropping-box");
    },
    "removeVisualClass": function (){
        if (pageDOD.visual_timer==0){
            $("html").removeClass("dropping");
            $(".img_selector_div, .imgs_selector_div").parent().parent().removeClass("dropping-box");
            pageDOD.visual_timer = 0;
        }else{
            pageDOD.visual_timer--;
            setTimeout(pageDOD.removeVisualClass, 1000);
        }
    },
    "onDrop": function (evt){
        var files = evt.dataTransfer.files;
        evt.preventDefault();
        pageDOD.visual_timer=0;
        $("html").removeClass("dropping");
        $(".img_selector_div, .imgs_selector_div").parent().parent().removeClass("dropping-box");
        debugger;
        if (files.length > 10){
            backend.message.insert("danger", "錯誤", "一次可上傳 10個文件", undefined);
            return;
        }
        for (var i=0; i<files.length; i++) {
            var t = evt.target;
            var randId = getRandID("upload-");
            if ($(t).hasClass("form-group")){
                $(t).attr("data-uploadId", randId);
            }else{
                $(t).parents(".form-group").attr("data-uploadId", randId);
            }
            if ($(t).hasClass("mce-content-body") || $(t).parents("body").hasClass('mce-content-body ')){
                randId = $(t).parents("body").data("id") || $(t).data("id");
                backend.uploader.addFile(files[i], randId, pageDOD.setEditorValue);
            }else{
                backend.uploader.addFile(files[i], randId, pageDOD.setTargetValue);
            }
        }
    },
    "setTargetValue": function (data){
        var url = data.response.url;
        var target_id = data.target_id;
        var t = $("*[data-uploadId='" + data.target_id + "']");
        t.find("input").first().val(data.response.url).show();
        if (url == ""){
            t.find(".img_selector_item").css("background-image", "none").addClass("img_selector_item_none");
        }else{
            t.find(".img_selector_item").css("background-image", "url(" + url + ")").removeClass("img_selector_item_none");
        }
    },
    "setEditorValue": function (data){
        var url = data.response.url;
        var target_id = data.target_id;
        if (tinyMCE.get(target_id)){
            tinyMCE.get(target_id).selection.setContent('<img src="' + url + '" />');
        }
    }
};
function change_lang(index){
    $("a.btn-lang").eq(index).click();
}

function create_editor(id){
    var ed = tinyMCE.createEditor(id, {
    theme : 'modern',
    content_css : ["/plugins/backend_ui_fuscata/static/TinyMCE/4.2.5/skins/lightgray/content.min.css"],
    height: 400,
    plugins: [
    "link image media code table preview hr anchor pagebreak textcolor fullscreen colorpicker "
    ],
    toolbar: "undo redo | styleselect | alignleft aligncenter alignright forecolor backcolor bold italic | link upload_image image media | code custom_fullscreen",
    statusbar: false,
    menubar: false,
    setup : function(ed) {
    if (typeof filepicker != 'undefined'){
        ed.addButton('upload_image', {
            title : '插入圖片',
            image : '/plugins/backend_ui_fuscata/static/TinyMCE/4.2.5/themes/upload_image.png',
            onclick : function() {
                var $target_editor = ed;
                start_filepicker($target_editor, true)
            }
        });
    }

    ed.addButton('custom_fullscreen', {
        title: '擴大編輯區',
        image : '/plugins/backend_ui_fuscata/static/TinyMCE/4.2.5/themes/fullscreen.png',
        onclick : function() {
            ed.execCommand('mceFullScreen');
        }
    });
    ed.on('init', function (e) {

    })
    },
    convert_urls:false,
    relative_urls:false,
    remove_script_host:false
    });
    ed.render();
}

function save_form(){
    var $form = $("form");
    $form.find(".field-type-rich-text-field").each(function(){
        var id = $(this).attr("id");
        if (tinyMCE.get(id)){
            $(this).val(tinyMCE.get(id).getContent());
        }
        $(this).change();
    });
    $form.submit();
}
function save_and_exit(){
    save_with_exit = true;
    save_form();
}
function scrollDiv(){
    $(".scrollDiv").addClass("on");
    backend.iframe.removeMask();
}

$(function () {
    if($("header").text().trim() != ""){
        $("body").addClass("has-header");
        $("header").stop().animate({
            top: 0
        }, 800);
        backend.affix(100);
    }else{
        $("body").addClass("no-header");
    }

    $(".scrollDiv").hover(function(){
        scrollDiv();
    }, function(){
        $(this).removeClass("on");
    }).mouseover(function(){
        scrollDiv();
    }).mouseleave(function() {
        $(this).removeClass("on");
    });
    //TODO if input has val addClass control-highlight

    if (window == top) {
        return;
    }
    //backend.iframe.afterOnLoad(location.pathname);
    $("#onLoad").remove();
    $('body').removeClass("body-hide");
    $(document).bind('click', function(e){
        backend.close_msg_nav();
    });
    $(document).bind('keydown', function (e) {
        console.log(e.which);
        if (e.ctrlKey && (e.which == 80)) {
            e.preventDefault();
            backend.print_iframe();
            return false;
        }
        if (e.ctrlKey && (e.which == 83)) {
            e.preventDefault();
            save_form();
            return false;
        }
        if ((e.ctrlKey && (e.which == 116)) || (e.which || e.keyCode) == 116) {
            e.preventDefault();
            backend.reload_iframe();
            return false;
        }
        if ((e.shiftKey && (e.which == 191))) {
            if (e.target.outerHTML.indexOf("<body") <0 && e.target.outerHTML.indexOf("<textarea") <0 || e.target.outerHTML.indexOf("<body") ==0) {
                e.preventDefault();
                console.log("help");
                return false;
            }
        }
        if (e.which == 191) {
            if (e.target.outerHTML.indexOf("<body") <0 && e.target.outerHTML.indexOf("<textarea") <0 || e.target.outerHTML.indexOf("<body") ==0) {
                e.preventDefault();
                console.log("search");
                return false;
            }
        }
        if (e.altKey && (e.which >= 49) && (e.which <= 57)) {
            e.preventDefault();
            change_lang(e.which - 49);
            return false;
        }


    });
    pageDOD.init();
    linkClickProcess();
    checkNavItemAndShow();

    $('#list-table').on('post-body.bs.table', function () {
        makeSortTable();
        makeListOp();
        checkNavItemAndShow();
        $(".sortable-list").removeClass("hidden");
    });
    try{
        $("iframe[name='iframeForm']").load(function(){
            var j = JSON.parse($(this).contents().find("body").text());
            $(".form-group").removeClass("has-error has-danger").find(".help-block").text("");
            var err = j["errors"];
            if (err){
                for (var key in err) {
                    $("form #" + key).parents(".form-group").addClass("has-error has-danger").find(".help-block").text(err[key]);
                }
                if ($("form").attr("action").indexOf("/_ah/upload/") >= 0){
                    $("form").attr("action", j["new_form_action"]);
                }
            }
            var msg = {
                "add": "記錄已新增",
                "edit": "記錄已儲存",
                "profile": "資料已更新",
                "undefined": "未定義的訊息"
            };
            if (j["response_info"] == "success"){
                if (save_with_exit){
                    setTimeout(backToList(), 10);
                    backend.message.quick_info(msg[j["response_method"]]);
                }else{
                    show_message(msg[j["response_method"]], 1800);
                }
            }else{
                backend.message.quick_info("表單欄位有誤");
            }
        });
        $(".submit_and_exit").click(function(){
            save_with_exit = true;
            $("form").submit();
        });
    }catch(e){

    }
    $(".img_selector_div input").on("change", function(){
        var val = $(this).val();
        $(this).parents(".img_selector_div").find(".img_selector_item").css("background-image", "url(" + val + ")");
        if ($(this).attr("id") == "avatar"){
            backend.set_avatar(location.href, val);
        }
    });

    $(".filepicker").click(function(){
        start_filepicker($(this).parents(".img_selector_div").find("input"))
    });

    tinyMCE.editors=[];
    $(".field-type-rich-text-field").each(function() {
        var label_name = $(this).prev().text();
        $(this).prev().remove();
        var id = $(this).attr("id");
        if (id == undefined){ id = $(this).attr("name"); $(this).attr("id", id); }
        if (id) {
            create_editor(id);
        }
    });
    window.onbeforeunload = function(){
        $(document).unbind();    //remove listeners on document
        $(document).find('*').unbind(); //remove listeners on all nodes
        //clean up cookies
        //remove items from localStorage
    }
});

// 處理頁面上的選單區塊
function checkNavItemAndShow(){
    // 預設為第一種語系欄位
    $("a.btn-lang").first().click();
    // 沒有 相關操作 項目的話，隱藏
    $(".list-operations").each(function(){
        if ($(this).find("li").length > 0){
            $(this).removeClass("hide");
        }else{
            $(this).addClass("hide");
        }
    });
    // 沒有項目的話，整個隱藏
    if ($(".nav-box li").length > 0){
        $(".nav-box").removeClass("hide").addClass("animated").addClass("fadeInUp");
    }
}
// 處理超連結按下時的動作
function linkClickProcess(){
    $("body").on("click", "a", function (e) {
        var _url = $(this).attr("href");
        if (_url === undefined){
            e.preventDefault();
            return;
        }
        // 切換語系
        if ($(this).hasClass("btn-lang")) {
            e.preventDefault();
            var lang = $(this).data("lang");
            $("div.lang").hide();
            $("div.lang.lang-" + lang).show();
            return;
        }
        // 刪除項目
        if ($(this).hasClass("btn-json-delete")) {
            e.preventDefault();
            swal({
                title: "您確定要刪除此記錄嗎",
                text: "删除後后将無法恢複，請谨慎操作！",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "删除",
                cancelButtonText: "取消",
                showLoaderOnConfirm: true,
                closeOnConfirm: false
            }, function () {
                json(_url, null, function (data) {
                    swal("删除成功！", "您已经永久删除了此記錄。", "success");
                    location.reload();
                }, function (data) {
                    swal("删除失敗！", "刪除記錄時發生問題。", "error");
                })
            });
            return;
        }
        // Json 操作
        if ($(this).hasClass("btn-json")) {
            e.preventDefault();
            var callback = $(this).data("callback");
            json(_url, null, function (data) {
                if (callback !== undefined){
                    eval(callback + '(' + JSON.stringify(data) + ')' );
                }else{
                    location.reload();
                }
            }, function(data){
                if (data.code == "404"){
                    show_message("找不到目標頁面");
                }else{
                    show_message(data.error);
                }
            });
            return;
        }
        // js 語法
        if (_url.indexOf("javascript:") <0 && _url.indexOf("#") <0 ){
            backend.iframe.load($(this).attr("href"), $(this).text(), location.pathname);
        }
    });
}
// 可以排序的表格
function makeSortTable(){
    try{
        $(".sortable-list tbody").sortable({
            placeholder: "ui-state-highlight",
            opacity: 0.8,
            //拖曳時透明
            cursor: 'move',
            //游標設定
            axis:'y',
            //只能垂直拖曳
            update : function () {
                var last_page_record = "";
                var $sort = $('.sortable-list tbody');
                $sort.find("tr").each(function() {
                    if ($(this).data("id") != undefined) {
                        last_page_record += "rec[]=" + $(this).data("id") + "&";
                    }
                });
                json_async("/admin/record/sort.json", last_page_record + $sort.sortable('serialize'), function (data) {
                    backend.message.quick_info("排序完成...");
                }, function (data) {
                    return false;
                });
            }
        });
    }catch(e){
    }
}
function makeListOp(){
    if ($(".filed-display-operations ul").data("done") == true){ return false;}
    $("input[data-field]").each(function () {
        var field_name = $(this).data("field");
        var field_texe = $(this).text();
        var field_val  = $(this).val();
        var is_checked = "checked" ? $(this).attr("checked"): "";
        if (field_name != 'is_enable' && field_name != 'record_buttons' && field_name != '') {
            $(".filed-display-operations ul").append(
                '<li><input type="checkbox" ' + is_checked + ' ' +
                'id="ro-field-' + field_name + '" ' +
                'value="' + field_val + '">' +
                '<label for="ro-field-' + field_name + '">' + $(this).parent().text() + '</label></li>'
            );
        }
    });
    $('.filed-display-operations ul input[type=checkbox]').change(function() {
        var id = $(this).attr("id").replace("ro-field-", "");
        var val = $(this).is(":checked");
        $("input[data-field='" + id + "']").click();
    });
    $(".filed-display-operations ul").attr("data-done", true);
}

function makeAjaxForm(){
    $('form').each(function(){
        if ($(this).hasClass("ajax_form") == false) {
            $(this).submit(function(event){
                event.stopPropagation();
                event.preventDefault();
                var data = $(this).serializeArray();
                $("#detailArea input:checkbox").each(function(){
                    if (this.checked == false) {
                        data[$(this).attr("name")] = "";
                    }
                });
                data["ajax_post"] = true;
                console.log($(this)[0]);
                var formData = new FormData($(this));
                console.log(formData);

                $.ajax({
                    url: $(this).attr("action"),  //server script to process data
                    type: 'POST',
                    // Ajax events
                    success: completeHandler = function(data) {
                        console.log(data);
                        /*
                        * Workaround for Chrome browser // Delete the fake path
                        */
                        if(navigator.userAgent.indexOf('Chrome')) {
                            var catchFile = $(":file").val().replace(/C:\\fakepath\\/i, '');
                        }
                        else {
                            var catchFile = $(":file").val();
                        }
                        var writeFile = $(":file");
                        writeFile.html(writer(catchFile));
                        //$("*setIdOfImageInHiddenInput*").val(data.logo_id);
                    },
                    error: errorHandler = function() {
                        alert("Something went wrong!");
                    },
                    // Form data
                    data: formData,
                    // Options to tell jQuery not to process data or worry about the content-type
                    cache: false,
                    contentType: false,
                    processData: false
                }, 'json');

                ajax_post($(this).attr("action"), data, function(page){
                    afterSubmit(page);
                }, function(page){
                    afterSubmit(page);
                });
            });

            $(this).addClass("ajax_form");
        }
    });
}
function afterSubmit(data){
    console.log(data);
}
