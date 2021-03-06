var MoveToRWD = (function (jQuery, d) {
    "use strict";
    var $ = jQuery;
    var host = "https://move-to-rwd.appspot.com";
    var client = window.location.hostname;  //.replace(/\./ig, "_").replace(/\-/ig, "_");
    var debug = true;
    //================================================== 載入元件 ==================================================
    function json(url,data,successCallback,errorCallback){$.ajax({url:url,type:"POST",dataType:"json",data:data,headers: {'X-Requested-With': 'XMLHttpRequest'},async:1,success:function(a){successCallback(a)},error:function(b,c,d){void 0==errorCallback?console.log(d.message):errorCallback(d.message)}})};
    // https://github.com/julien-maurel/jQuery-Storage-API/blob/master/jquery.storageapi.js                  Version: 1.9.1
    !function(e){"function"==typeof define&&define.amd?define(["jquery"],e):e("object"==typeof exports?require("jquery"):jQuery)}(function(e){function t(){var t,r,i,o=this._type,n=arguments.length,s=window[o],a=arguments,l=a[0];if(1>n)throw new Error("Minimum 1 argument must be given");if(e.isArray(l)){r={};for(var f in l){t=l[f];try{r[t]=JSON.parse(s.getItem(t))}catch(c){r[t]=s.getItem(t)}}return r}if(1!=n){try{r=JSON.parse(s.getItem(l))}catch(c){throw new ReferenceError(l+" is not defined in this storage")}for(var f=1;n-1>f;f++)if(r=r[a[f]],void 0===r)throw new ReferenceError([].slice.call(a,1,f+1).join(".")+" is not defined in this storage");if(e.isArray(a[f])){i=r,r={};for(var h in a[f])r[a[f][h]]=i[a[f][h]];return r}return r[a[f]]}try{return JSON.parse(s.getItem(l))}catch(c){return s.getItem(l)}}function r(){var t,r,i=this._type,o=arguments.length,n=window[i],s=arguments,a=s[0],l=s[1],f={};if(1>o||!e.isPlainObject(a)&&2>o)throw new Error("Minimum 2 arguments must be given or first parameter must be an object");if(e.isPlainObject(a)){for(var c in a)t=a[c],e.isPlainObject(t)||this.alwaysUseJson?n.setItem(c,JSON.stringify(t)):n.setItem(c,t);return a}if(2==o)return"object"==typeof l||this.alwaysUseJson?n.setItem(a,JSON.stringify(l)):n.setItem(a,l),l;try{r=n.getItem(a),null!=r&&(f=JSON.parse(r))}catch(h){}r=f;for(var c=1;o-2>c;c++)t=s[c],r[t]&&e.isPlainObject(r[t])||(r[t]={}),r=r[t];return r[s[c]]=s[c+1],n.setItem(a,JSON.stringify(f)),f}function i(){var t,r,i=this._type,o=arguments.length,n=window[i],s=arguments,a=s[0];if(1>o)throw new Error("Minimum 1 argument must be given");if(e.isArray(a)){for(var l in a)n.removeItem(a[l]);return!0}if(1==o)return n.removeItem(a),!0;try{t=r=JSON.parse(n.getItem(a))}catch(f){throw new ReferenceError(a+" is not defined in this storage")}for(var l=1;o-1>l;l++)if(r=r[s[l]],void 0===r)throw new ReferenceError([].slice.call(s,1,l).join(".")+" is not defined in this storage");if(e.isArray(s[l]))for(var c in s[l])delete r[s[l][c]];else delete r[s[l]];return n.setItem(a,JSON.stringify(t)),!0}function o(t){var r=a.call(this);for(var o in r)i.call(this,r[o]);if(t)for(var o in e.namespaceStorages)l(o)}function n(){var r=arguments.length,i=arguments,o=i[0];if(0==r)return 0==a.call(this).length;if(e.isArray(o)){for(var s=0;s<o.length;s++)if(!n.call(this,o[s]))return!1;return!0}try{var l=t.apply(this,arguments);e.isArray(i[r-1])||(l={totest:l});for(var s in l)if(!(e.isPlainObject(l[s])&&e.isEmptyObject(l[s])||e.isArray(l[s])&&!l[s].length)&&l[s])return!1;return!0}catch(f){return!0}}function s(){var r=arguments.length,i=arguments,o=i[0];if(1>r)throw new Error("Minimum 1 argument must be given");if(e.isArray(o)){for(var n=0;n<o.length;n++)if(!s.call(this,o[n]))return!1;return!0}try{var a=t.apply(this,arguments);e.isArray(i[r-1])||(a={totest:a});for(var n in a)if(void 0===a[n]||null===a[n])return!1;return!0}catch(l){return!1}}function a(){var e=this._type,r=arguments.length,i=window[e],o=arguments,n=[],s={};if(s=r>0?t.apply(this,o):i,s&&s._cookie)for(var a in Cookies.get())""!=a&&n.push(a.replace(s._prefix,""));else for(var l in s)s.hasOwnProperty(l)&&n.push(l);return n}function l(t){if(!t||"string"!=typeof t)throw new Error("First parameter must be a string");u?(window.localStorage.getItem(t)||window.localStorage.setItem(t,"{}"),window.sessionStorage.getItem(t)||window.sessionStorage.setItem(t,"{}")):(window.localCookieStorage.getItem(t)||window.localCookieStorage.setItem(t,"{}"),window.sessionCookieStorage.getItem(t)||window.sessionCookieStorage.setItem(t,"{}"));var r={localStorage:e.extend({},e.localStorage,{_ns:t}),sessionStorage:e.extend({},e.sessionStorage,{_ns:t})};return"object"==typeof Cookies&&(window.cookieStorage.getItem(t)||window.cookieStorage.setItem(t,"{}"),r.cookieStorage=e.extend({},e.cookieStorage,{_ns:t})),e.namespaceStorages[t]=r,r}function f(e){var t="jsapi";try{return window[e]?(window[e].setItem(t,t),window[e].removeItem(t),!0):!1}catch(r){return!1}}var c="ls_",h="ss_",u=f("localStorage"),g={_type:"",_ns:"",_callMethod:function(e,t){var r=[],t=Array.prototype.slice.call(t),i=t[0];return this._ns&&r.push(this._ns),"string"==typeof i&&-1!==i.indexOf(".")&&(t.shift(),[].unshift.apply(t,i.split("."))),[].push.apply(r,t),e.apply(this,r)},alwaysUseJson:!1,get:function(){return this._callMethod(t,arguments)},set:function(){var t=arguments.length,i=arguments,o=i[0];if(1>t||!e.isPlainObject(o)&&2>t)throw new Error("Minimum 2 arguments must be given or first parameter must be an object");if(e.isPlainObject(o)&&this._ns){for(var n in o)this._callMethod(r,[n,o[n]]);return o}var s=this._callMethod(r,i);return this._ns?s[o.split(".")[0]]:s},remove:function(){if(arguments.length<1)throw new Error("Minimum 1 argument must be given");return this._callMethod(i,arguments)},removeAll:function(e){return this._ns?(this._callMethod(r,[{}]),!0):this._callMethod(o,[e])},isEmpty:function(){return this._callMethod(n,arguments)},isSet:function(){if(arguments.length<1)throw new Error("Minimum 1 argument must be given");return this._callMethod(s,arguments)},keys:function(){return this._callMethod(a,arguments)}};if("object"==typeof Cookies){window.name||(window.name=Math.floor(1e8*Math.random()));var m={_cookie:!0,_prefix:"",_expires:null,_path:null,_domain:null,setItem:function(e,t){Cookies.set(this._prefix+e,t,{expires:this._expires,path:this._path,domain:this._domain})},getItem:function(e){return Cookies.get(this._prefix+e)},removeItem:function(e){return Cookies.remove(this._prefix+e,{path:this._path})},clear:function(){for(var t in Cookies.get())""!=t&&(!this._prefix&&-1===t.indexOf(c)&&-1===t.indexOf(h)||this._prefix&&0===t.indexOf(this._prefix))&&e.removeCookie(t)},setExpires:function(e){return this._expires=e,this},setPath:function(e){return this._path=e,this},setDomain:function(e){return this._domain=e,this},setConf:function(e){return e.path&&(this._path=e.path),e.domain&&(this._domain=e.domain),e.expires&&(this._expires=e.expires),this},setDefaultConf:function(){this._path=this._domain=this._expires=null}};u||(window.localCookieStorage=e.extend({},m,{_prefix:c,_expires:3650}),window.sessionCookieStorage=e.extend({},m,{_prefix:h+window.name+"_"})),window.cookieStorage=e.extend({},m),e.cookieStorage=e.extend({},g,{_type:"cookieStorage",setExpires:function(e){return window.cookieStorage.setExpires(e),this},setPath:function(e){return window.cookieStorage.setPath(e),this},setDomain:function(e){return window.cookieStorage.setDomain(e),this},setConf:function(e){return window.cookieStorage.setConf(e),this},setDefaultConf:function(){return window.cookieStorage.setDefaultConf(),this}})}e.initNamespaceStorage=function(e){return l(e)},u?(e.localStorage=e.extend({},g,{_type:"localStorage"}),e.sessionStorage=e.extend({},g,{_type:"sessionStorage"})):(e.localStorage=e.extend({},g,{_type:"localCookieStorage"}),e.sessionStorage=e.extend({},g,{_type:"sessionCookieStorage"})),e.namespaceStorages={},e.removeAllStorages=function(t){e.localStorage.removeAll(t),e.sessionStorage.removeAll(t),e.cookieStorage&&e.cookieStorage.removeAll(t),t||(e.namespaceStorages={})},e.alwaysUseJsonInStorage=function(t){g.alwaysUseJson=t,e.localStorage.alwaysUseJson=t,e.sessionStorage.alwaysUseJson=t,e.cookieStorage&&(e.cookieStorage.alwaysUseJson=t)}});
    //================================================== 相關設置 ==================================================
    function load_file(url, id){
        if (url.indexOf(".css") > 0){
            var m2css = d.createElement('link');
            m2css.setAttribute('type', 'text/css');
            m2css.setAttribute('rel', 'stylesheet');
            m2css.setAttribute('id', id);
            m2css.setAttribute('href', url);
            d.body.appendChild(m2css);
        }
        if (url.indexOf(".js") > 0){
            var m2js = d.createElement('script');
            m2js.setAttribute('type', 'text/javascript');
            m2js.setAttribute('id', 'move-to-rwd-js');
            m2js.setAttribute('charset', 'UTF-8');
            m2js.setAttribute('src', url);
            d.body.appendChild(m2js);
        }
    }
    load_file(host + '/js/slidebars/slidebars.min.css', "'slidebars-css'");
    load_file(host + '/js/slidebars/slidebars.min.js', "'slidebars-js'");
    json(host+'/' + client + '/info.json', null, function(data){
        var js_vision = data["js-vision"];
        var css_vision = data["css-vision"];
        var vision = data["vision"];
        load_file(host + '/' + client + '/' + css_vision + '/rwd.css?r=' + vision, "'move-to-rwd-css'");
        load_file(host + '/' + client + '/' + js_vision + '/rwd.js?r=' + vision, "'move-to-rwd-js'");
    });
    window["MoveToRWD"] = undefined;
});
// 確認 jq 的可用性
function check_if_jquery_is_ready() {
    if (typeof jQuery !== "undefined") {
        jQuery(function () {
            MoveToRWD(jQuery, document);
        });
    } else {
        setTimeout(check_if_jquery_is_ready, 50);
    }
}
// 載入相關資源
(function (d) {
    if (typeof jQuery === "undefined" && typeof $ === "undefined") {
        var hasJQ = false;
        var scripts = document.getElementsByTagName("script");
        var i = 0;
        for (i = 0; i < scripts.length; i++) {
            if (scripts[i].src.indexOf("jquery") > 0) {
                hasJQ = true;
            }
        }
        if (hasJQ === false) {
            var e = d.createElement('script');
            e.setAttribute('type', 'text/javascript');
            e.setAttribute('id', 'jquery-1-11-1');
            e.setAttribute('charset', 'UTF-8');
            e.setAttribute('src', 'http://code.jquery.com/jquery-1.11.1.min.js');
            d.body.appendChild(e);
        }
    }
    setTimeout(check_if_jquery_is_ready, 10);
})(document);

