/**
 *
 */

define([
    'dojo/_base/declare',
    'put-selector/put',
    'dojo/query',
    'gtcms/session',
    'gtcms/AdminLoginForm',
    'dijit/Dialog',
    'dojo/NodeList-dom', // for query(…).orphan()
    'xstyle/css!/_css/gtlogo.css'
], function (
    declare, put, query,
    session, AdminLoginForm, Dialog
) {
    var _Dialog = declare(
        [Dialog], {
            gtModal: false,
            startup: function () {
                this.inherited(arguments);

                if (this.get('gtModal')) {
                    query('.dijitDialogCloseIcon', this.domNode).orphan();
                }
                else {
                    query('.dijitDialogTitleBar', this.domNode).style({paddingRight: '26px'});
                }
                var titleNode = query('.dijitDialogTitle', this.domNode)[0];
                put(titleNode, 'div.gtsymbol.small[style=$]',
                    "font-size: 14px; float: left; margin-right: 4px;");
                put(titleNode,
                    'div[style=$]',
                    'float: right; color: rgba(0, 0, 255, 0.25);'+
                    ' font-size: 10px; text-shadow: 1px 1px 0px white;',
                    'gtCMS');
            }
        }
    );

    var dialog;
    var mainLoop = function mainLoop() {
        session.status(true).then(
            function (sess) {
                if (!sess.authorized) {
                    if (!dialog) {
                        dialog = new _Dialog({
                            title: 'Logowanie',
                            gtModal: true,
                            content: new AdminLoginForm({
                                onLogin: function () {
                                    dialog.hide();
                                }
                            }),
                            onHide: mainLoop
                        });
                    }
                    dialog.show();
                }
                else {
                    require(sess.imports, function() {
                        for(var i in arguments) {
                            if (typeof arguments[i].run == 'function') {
                                arguments[i].run();
                            }
                        }
                    });
                }
            }
        );
    };
    mainLoop();
    return {};
});
