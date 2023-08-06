/**
 */

define([
    'dojo/_base/declare',
    'dojo/_base/window',
    'dojo/dom-style',
    'dojo/parser',
    'dojo/on',
    'dijit/_WidgetBase',
    'dijit/_TemplatedMixin',
    'put-selector/put',
    'dojo/text!./templates/LoginDialog.html',
    'gtcms/UserLoginLite' // needed by template
], function(
    declare, win, domStyle, parser,
    on, _WidgetBase, _TemplatedMixin,
    put, template
) {
    var idcounter=0;
    return declare(
        [ _WidgetBase ], {
            target: '',
            constructor: function(args, domNode) {
                var self = this;
                if (domNode.id === "") {
                    domNode.id = 'UserLoginLite_'+(idcounter++);
                }
                on(domNode, 'click', function (event) {
                    event.preventDefault();
                    event.stopPropagation();
                    if (!self.pane) {
                        self.pane = put(win.body(), 'div.login-pane');
                        template = template.replace(/\${target}/g, self.target);
                        self.pane.innerHTML = template;
                        parser.parse(self.pane).then(function(elems) {console.log(elems);});
                        on(self.pane, 'click', function (event) {
                            domStyle.set(self.pane, 'display', 'none');
                        });
                        on(self.pane.firstChild, 'click', function (event) {
                            event.stopPropagation();
                        });
                    }
                    domStyle.set(self.pane, 'display', 'block');
                });
            }
        });
});
