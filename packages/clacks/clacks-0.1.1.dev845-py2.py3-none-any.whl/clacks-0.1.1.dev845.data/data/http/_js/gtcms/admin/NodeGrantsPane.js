/*
 * NodeGrantsPane.js
 */

define([
    'dojo/_base/declare',
    'dojo/on',
    'dojo/dom-geometry',
    'dijit/layout/ContentPane',
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    'dojo/text!../templates/NodeGrantsPane.html',
    'gtcms/stores/siteNodes',
    'gtcms/session',
    //needed by template:
    'gtcms/admin/GrantSelect'
], function (
    declare, on, domGeom,
    ContentPane,
    _TemplatedMixin, _WidgetsInTemplateMixin,
    template, siteNodesStore, session
) {

    function _(txt) {return txt;}

    return declare([ContentPane, _TemplatedMixin, _WidgetsInTemplateMixin], {
        templateString: template,

        _setSiteNodeAttr: function (siteNode) {
            this._set('siteNode', siteNode);
            var that = this;
            siteNodesStore.get(this.siteNode).then(function (node) {
                that._view_grant.set('value', node.viewGrant);
                that._edit_grant.set('value', node.editGrant);
                that._add_node_grant.set('value', node.addNodeGrant);
            });
        },

        _setControlAttr: function (control) {
            this._set('control', control);
            if (control) {
                this.set('siteNode', control._page);
            }
        },

        submit: function () {
            if (session.granted('SITE_ADMIN')) {
                return siteNodesStore.put({
                    id: this.siteNode,
                    viewGrant: this._view_grant.get('value'),
                    editGrant: this._edit_grant.get('value'),
                    addNodeGrant: this._add_node_grant.get('value')
                }).then(function () {});
            }
            return false;
        },

        postCreate: function () {
            this.inherited(arguments);

            var that = this;

            function errorMsg(message) {
                that._msg.innerHTML = 'ERROR: '+message;
                that._msg.style.color = 'red';
                setTimeout(function () {
                    that._msg.innerHTML = '';
                }, 5000);
            }

            //this._addresses.set('content', grid.domNode);
            if (!session.granted('SITE_ADMIN')) {
                this._view_grant.set('readOnly', true);
                this._edit_grant.set('readOnly', true);
                this._add_node_grant.set('readOnly', true);
            }
        }
    });
});
