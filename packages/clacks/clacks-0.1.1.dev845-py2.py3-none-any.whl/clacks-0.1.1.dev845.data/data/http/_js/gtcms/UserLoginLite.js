/**
 * this widget needs to be assigned declaratively to a form element
 * containing exactly three inputs, in order: login, password, submit
 * widget adds to it div element with status message with progress and
 * if authorization is not successful
 */

define([
    'dojo/_base/declare',
    'dojo/on',
    'dijit/_WidgetBase',
    'put-selector/put',
    'gtcms/session'
], function(
    declare, on, _WidgetBase,
    put, session
) {
    var idcounter=0;
    return declare(
        [ _WidgetBase ], {
            constructor: function(args, domNode) {
                var self=this;

/* if (domNode instanceof HTMLFormElement) {
                    on(domNode, 'submit', function (event)  {
                        event.preventDefault();
                        return false
                    });
                }*/
                on(domNode, 'submit', function (event) {
                    event.preventDefault();
                    event.stopPropagation();
                    var loginTag = domNode.querySelector('[name=login]');
                    var passwordTag = domNode.querySelector('[name=password]');
                    session.login(loginTag.value, passwordTag.value).then(
                        function (status) {
                            if (!status.authorized) {
                                var message = 'Błędny login lub hasło';
                                if (status.message) {
                                    message = status.message;
                                }
                                var msg = put(domNode, 'div[style=$] $', 'color: red', message);
                                setTimeout(function () { put(msg, '!'); }, 3000);
                            }
                            else {
                                if (self.target && self.target.length) {
                                    location = self.target;
                                }
                                else {
                                    location.reload(true);
                                }
                            }
                        });
                });
            }
        });
});
