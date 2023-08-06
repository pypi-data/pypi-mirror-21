define([
    'dojo/_base/declare',
    'dojo/when',
    'dojo/_base/xhr',
    'gtcms/session',
    'dijit/focus',
    'dijit/_Widget',
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    'dojo/text!../templates/ToolBox.html',
    'dijit/form/Form',
    'dijit/form/Button',
    'dijit/form/TextBox'
], function(
    declare, when, xhr, session, dijitFocus,
    _Widget, _Templated, _WidgetsInTemplate, template
) {
    return declare(
        [_Widget, _Templated, _WidgetsInTemplate], {
            templateString: template,

            userName: '',
            _setUserNameAttr: {node: '_userName', type: 'innerHTML'},

            onLogout: function() {},

            constructor: function () {
                var that = this;
                this.inherited('constructor', arguments);
            },

            postCreate: function () {
                var that=this;
                this._logoutBtn.onClick = function() {
                    session.logout().then(function() {
                        that.onLogout();
                    });
                };

                xhr.post({
                    url: "/_ajax/ToolBox/getContent/",
                    content: {url: window.location.pathname},
                    handleAs: 'json'
                }).then(function(response) {
                    that._compatActions.innerHTML = response.content;
                });
            },

            buildRenering: function () {
                this.inherited("buildRendering", arguments);
            },

            setFocus: function () {
                var that=this;

                dijitFocus.focus(this._logoutBtn.focusNode);

                when(session.status(), function(sess) {
                    that.set('userName', sess.username);
                });
            }
        }
    );
});
