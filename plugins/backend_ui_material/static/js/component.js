/*!
 * remark (http://getbootstrapadmin.com/remark)
 * Copyright 2015 amazingsurge
 * Licensed under the Themeforest Standard Licenses
 */
$.components.register("TouchSpin",{mode:"default",defaults:{verticalupclass:"md-plus",verticaldownclass:"md-minus",buttondown_class:"btn btn-default",buttonup_class:"btn btn-default"}});
/*!
 * Remark (http://getbootstrapadmin.com/remark)
 * Copyright 2015 amazingsurge
 * Licensed under the Themeforest Standard Licenses
 */
$.components.register("nestable",{mode:"default"});
/*!
 * yooliang moment
 * 侑良時間組件
 * Version 1.00 (01/09/2016
 * Copyright (c) 2016 Qi-Liang Wen
 */
$.components.register("moment",{mode:"init",init:function(a,b){if(!moment){return}b=b||"zh-tw";moment.locale(b);$(".moment").each(function(){var d=$(this).data("datetime");d=d||$(this).text();$(this).data("datetime",d);if($(this).data("moment-func")=="fromNow"){var e=moment(d,"YYYY-MM-DD hh:mm:ss");$(this).text(moment(e._d).fromNow())}})}});
/*!
 * remark (http://getbootstrapadmin.com/remark)
 * Copyright 2015 amazingsurge
 * Licensed under the Themeforest Standard Licenses
 */
$.components.register("scrollable",{mode:"init",defaults:{namespace:"scrollable",contentSelector:"> [data-role='content']",containerSelector:"> [data-role='container']"},init:function(context){if($.fn.asScrollable){var defaults=$.components.getDefaults("scrollable");$('[data-plugin="scrollable"]',context).each(function(){var options=$.extend({},defaults,$(this).data());$(this).asScrollable(options)})}}});
/*!
 * remark (http://getbootstrapadmin.com/remark)
 * Copyright 2015 amazingsurge
 * Licensed under the Themeforest Standard Licenses
 */
$.components.register("slidePanel",{mode:"manual",defaults:{closeSelector:".slidePanel-close",mouseDragHandler:".slidePanel-handler",loading:{template:function(options){return'<div class="'+options.classes.loading+'"><div class="loader loader-default"></div></div>'},showCallback:function(options){this.$el.addClass(options.classes.loading+"-show")},hideCallback:function(options){this.$el.removeClass(options.classes.loading+"-show")}}}});
/*!
 * remark (http://getbootstrapadmin.com/remark)
 * Copyright 2015 amazingsurge
 * Licensed under the Themeforest Standard Licenses
 */
$.components.register("verticalTab",{mode:"init",init:function(context){$.fn.matchHeight&&$(".nav-tabs-vertical",context).each(function(){$(this).children().matchHeight()})}}),$.components.register("horizontalTab",{mode:"init",init:function(context){$.fn.responsiveHorizontalTabs&&$(".nav-tabs-horizontal",context).responsiveHorizontalTabs()}}),$.components.register("navTabsLine",{mode:"init",defaults:{speed:"0.5s, 1s",animate:"cubic-bezier(0.4, 0, 0.2, 1), cubic-bezier(0.4, 0, 0.2, 1)",tpl:function(){return'<li class="nav-tabs-autoline"></li>'}},init:function(context){var defaults=$.components.getDefaults("navTabsLine");$(".nav-tabs-line",context).each(function(){var $this=$(this),options=$.extend({},defaults,$this.data()),$parent=$this.parent(),$active=$this.find(".active"),$autoLineTpl=$(options.tpl()).css({"-webkit-transition-duration":options.speed,"transition-duration":options.speed,"-webkit-transition-timing-function":options.animate,"transition-timing-function":options.animate});$autoLineTpl.appendTo($this);var horizontalLine=function($this){var left=$this.position().left,lineWidth=$this.width();$autoLineTpl.css({left:left,width:lineWidth})},verticalLine=function($this){var top=$this.position().top,lineHeight=$this.height();$autoLineTpl.css({top:top,height:lineHeight})},change=function($this){$parent.hasClass("nav-tabs-vertical")?verticalLine($this):horizontalLine($this)};$this.on("shown.bs.tab",'a[data-toggle="tab"]',function(){change($(this).parent())}),change($active)})}});
/*!
 * remark (http://getbootstrapadmin.com/remark)
 * Copyright 2015 amazingsurge
 * Licensed under the Themeforest Standard Licenses
 */
$.components.register("placeholder",{mode:"init",init:function(context){$.fn.placeholder&&$("input, textarea",context).placeholder()}});
/*!
 * remark (http://getbootstrapadmin.com/remark)
 * Copyright 2015 amazingsurge
 * Licensed under the Themeforest Standard Licenses
 */
$.components.register("material",{init:function(context){$(".form-material",context).each(function(){var $this=$(this);if($this.data("material")!==!0){var $control=$this.find(".form-control");if($control.attr("data-hint")&&$control.after("<div class=hint>"+$control.attr("data-hint")+"</div>"),$this.hasClass("floating")){if($control.hasClass("floating-label")){var placeholder=$control.attr("placeholder");$control.attr("placeholder",null).removeClass("floating-label"),$control.after("<div class=floating-label>"+placeholder+"</div>")}(null===$control.val()||"undefined"==$control.val()||""===$control.val())&&$control.addClass("empty")}$control.next().is("[type=file]")&&$this.addClass("form-material-file"),$this.data("material",!0)}})},api:function(){function _isChar(e){return"undefined"==typeof e.which?!0:"number"==typeof e.which&&e.which>0?!e.ctrlKey&&!e.metaKey&&!e.altKey&&8!=e.which&&9!=e.which:!1}$(document).on("keydown.site.material paste.site.material",".form-control",function(e){_isChar(e)&&$(this).removeClass("empty")}).on("keyup.site.material change.site.material",".form-control",function(){var $this=$(this);""===$this.val()&&"undefined"!=typeof $this[0].checkValidity&&$this[0].checkValidity()?$this.addClass("empty"):$this.removeClass("empty")}).on("focus",".form-material-file",function(){$(this).find("input").addClass("focus")}).on("blur",".form-material-file",function(){$(this).find("input").removeClass("focus")}).on("change",".form-material-file [type=file]",function(){var value="";$.each($(this)[0].files,function(i,file){value+=file.name+", "}),value=value.substring(0,value.length-2),value?$(this).prev().removeClass("empty"):$(this).prev().addClass("empty"),$(this).prev().val(value)})}});
/*!
 * remark (http://getbootstrapadmin.com/remark)
 * Copyright 2015 amazingsurge
 * Licensed under the Themeforest Standard Licenses
 */
$.components.register("toastr",{mode:"api",api:function(){if("undefined"!=typeof toastr){var defaults=$.components.getDefaults("toastr");$(document).on("click.site.toastr",'[data-plugin="toastr"]',function(e){e.preventDefault();var $this=$(this),options=$.extend(!0,{},defaults,$this.data()),message=options.message||"",type=options.type||"info",title=options.title||void 0;switch(type){case"success":toastr.success(message,title,options);break;case"warning":toastr.warning(message,title,options);break;case"error":toastr.error(message,title,options);break;case"info":toastr.info(message,title,options);break;default:toastr.info(message,title,options)}})}}});