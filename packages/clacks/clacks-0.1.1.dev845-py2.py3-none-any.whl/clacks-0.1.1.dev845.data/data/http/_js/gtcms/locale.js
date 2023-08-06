/*
 * locales.js
 */

define([
], function() {
    var proxied = window.XMLHttpRequest.prototype.open;
    var lang = document.getElementsByTagName('html')[0].lang || ''
    window.XMLHttpRequest.prototype.open = function() {
        result = proxied.apply(this, [].slice.call(arguments));
        if (lang)
            this.setRequestHeader('Accept-Language', lang);
        return result
    };

    return {
        _: function (text) {return text;}} // dumb temporary implementation
    ;
});
