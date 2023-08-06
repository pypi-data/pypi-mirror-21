/**
 * this widget needs to be assigned declaratively to a form element
 * containing at least one input type element, where only first one is used
 */

define([
    'dojo/_base/declare',
    'dojo/on',
    'dijit/_WidgetBase',
    'dijit/_TemplatedMixin',
    'put-selector/put',
    'gtcms/session'
], function(
    declare, on, _WidgetBase, _TemplatedMixin,
    put, session
) {
    var idcounter=0;
    return declare(
        [ _WidgetBase ], {
            constructor: function(args, domNode) {
                if (!domNode.id) {
                    domNode.id = 'UserLoginLite_'+(idcounter++);

                }
                this.inherited(arguments);
                on(domNode[0] || domNode, 'click', function (event) {
                    event.preventDefault();
                    event.stopPropagation();

                    session.logout().then(
                        function () {
                            location.reload(true);
                        });
                });
            }
        });
});
