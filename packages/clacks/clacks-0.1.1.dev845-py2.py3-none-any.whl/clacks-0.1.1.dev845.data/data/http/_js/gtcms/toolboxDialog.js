/**
 *
 */

define([
    'dojo/dom',
    'dojo/_base/window',
    'gtcms/session',
    'put-selector/put',
    'xstyle/css!/_js/dijit/themes/claro/claro.css'
], function (
    dom, win, session, put
) {
    var state = false;
    var _dialogs = {};
    var _activeDlg;
    var tbxBtn = dom.byId('toolbox-button');
    put(win.body(), '.claro');
    var _toggle = function () {
        if (!state) {
            session.status(true).then(
                function(status) {
                    var dialogType = (status.authorized ?
                        status.toolboxJS : 'gtcms/AdminLoginForm');

                    require(
                        [dialogType, 'dijit/popup', 'dijit/TooltipDialog'],
                        function(DialogForm, popup, TooltipDialog) {
                            var dialogForm;

                            var _refresh = function() {
                                popup.close(_activeDlg);
                                state = false;
                                _toggle();
                            };

                            if (!_dialogs[dialogType]) {
                                if (status.authorized) {
                                    dialogForm = new DialogForm({
                                        onLogout: _refresh
                                    });
                                }
                                else {
                                    dialogForm = new DialogForm({
                                        onLogin: _refresh,
                                        formTitle: 'Toolbox'
                                    });
                                }
                                _dialogs[dialogType] = new TooltipDialog({
                                    content: dialogForm,
                                    onBlur: function() {
                                        popup.close(_dialogs[dialogType]);
                                        state = !state;
                                    },
                                    onShow: function () {
                                        this.inherited('onShow', arguments);
                                        dialogForm.setFocus();
                                    }
                                });
                            }
                            if (_activeDlg) {
                                popup.close(_activeDlg);
                                _activeDlg = undefined;
                            }
                            _activeDlg = _dialogs[dialogType];
                            popup.open({ popup: _activeDlg, x: 0, y: 0});
                        });
                }
            );
        }
        else {
            if (_activeDlg) {
                require(['dijit/popup'], function(popup) {
                    popup.close(_activeDlg);
                    _activeDlg = undefined;
                });
            }
        }
        state = !state;
    };
    return {toggle: _toggle};
});
