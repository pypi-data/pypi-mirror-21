define([
    'dojo/_base/declare',
    'dojo/_base/json',
    'dojo/_base/fx',
    'dojo/parser',
    'dojo/dom-form',
    'dojo/dom-style',
    'gtcms/session',
    'dijit/focus',
    'dijit/_Widget',
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    'dojo/text!./templates/AdminLoginForm.html',
    // needed by template
    'dijit/form/Form',
    'dijit/form/Button',
    'dijit/form/TextBox'
], function (
    declare, dojo, fx, parser, domForm, domStyle, session, dijitFocus,
    _Widget, _Templated, _WidgetsInTemplate, template
) {
    return declare(
        'gtcms.AdminLoginForm',
        [_Widget, _Templated, _WidgetsInTemplate],
        {
            templateString: template,
            formTitle: '',
            _setFormTitleAttr: function(title) {
                this._formTitle.innerHTML = title;
                domStyle.set(this._formTitleBox, 'display', title.length ? 'block' : 'none');
            },

            onLogin: function() {},

            postCreate: function () {
                var that=this;

                this.inherited('postCreate', arguments);
                this._formNode.set('onSubmit', function () {
                    var fData = domForm.toObject(that._formNode.id);
                    that._submitBtn.set('disabled', true);
                    that._messageBox.innerHTML = 'Trwa weryfikacja...';
                    domStyle.set(that._messageBox, 'opacity', '1');
                    fx.fadeOut({node: that._messageBox, duration: 3000}).play();
                    session.login(fData.login, fData.password).then(
                        function (status) {
                            if (!status.authorized) {
                                if (status.message) {
                                    that._messageBox.innerHTML = status.message;
                                }
                                else {
                                    that._messageBox.innerHTML = 'Błędny login lub hasło';
                                }
                                domStyle.set(that._messageBox, 'opacity', '1');
                                fx.fadeOut({node: that._messageBox, duration: 3000}).play();
                            }
                            else {
                                that.onLogin();
                            }
                            that._submitBtn.set('disabled', false);
                        });
                    return false;
                });
            },

            buildRenering: function () {
                var result = this.inherited('buildRendering', arguments);
                return result;
            },
            setFocus: function () {
                dijitFocus.focus(this.focusNode.focusNode);
            }
        });
});
