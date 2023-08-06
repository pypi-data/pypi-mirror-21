/*
 * ArticleListPane.js
 */

define([
    'dojo/_base/declare',
    'dijit/layout/LayoutContainer',
    'dijit/layout/ContentPane',
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    'dijit/form/Button',
    'gtcms/admin/panel',
    'gtcms/dstores/siteNodes',
    'gtcms/stores/pagePlacements',
    'dojo/text!./templates/ArticleListPane.html',
    //needed by template:
    'dijit/TitlePane',
    'dijit/form/TextBox',
    'dijit/form/RadioButton',
    'dijit/form/Select',
    'gtcms/admin/PageSelect',
    'gtcms/admin/GrantSelect'
], function (
    declare,
    LayoutContainer, ContentPane,
    _Templated, _WidgetsInTemplate, Button,
    panel, store, placementsStore,
    template
) {
    var mainPane = {};
    var openPane = function (linkid) {
        store.get(linkid).then(function (link) {
            var messagePane, boxPane;
            if (!mainPane[linkid]) {
                mainPane[linkid] = new LayoutContainer({
                    gutters: false,
                    title: link.linkName || 'Link',
                    closable: true,
                    onClose: function () {
                        mainPane[linkid] = undefined;
                        return true;
                    }
                });

                var setContents = function (pane) {
                    pane._linkName.set('value', link.linkName);
                    pane._urlPart.set('value', link.urlPart);
                    pane._visible.set('checked', link.visible);
                    pane._isBase.set('checked', link.isBase);
                    pane._targetUrl.href = link.url;
                    pane._targetUrl.innerHTML = link.url;
                    pane._placement.set('value', link.placement);
                    pane._edit_grant.set('value', link.editGrant)
                    pane._view_grant.set('value', link.viewGrant);
                    pane._add_node_grant.set('value', link.addNodeGrant);
                };

                boxPane = declare([ContentPane, _Templated, _WidgetsInTemplate], {
                    templateString: template,
                    region: 'center',
                    style: "border-width: 0px",

                    postCreate: function() {
                        this.inherited(arguments);
                    },
                    startup: function () {
                        this.inherited(arguments);
                        this._placement.set('labelAttr', 'label');
                        this._placement.setStore(placementsStore, link.style,
                                                 {query: {page: linkid}});
                        setContents(this);
                    }
                })();

                var submit = new Button({
                    label: 'Zapisz zmiany',
                    region: 'right',
                    style: 'border-width: 0px; margin: 0px 8px 10px 5px;',
                    onClick: function () {
                        if (boxPane.form.validate()) {

                            messagePane.set('content', 'Zapisywanie zmian');
                            var toUpdate = {
                                id: linkid,
                                linkName: boxPane._linkName.get('value'),
                                urlPart: boxPane._urlPart.value,
                                visible: boxPane._visible.checked,
                                isBase: boxPane._isBase.checked,
                                placement: boxPane._placement.get('value'),
                                viewGrant: boxPane._view_grant.get('value'),
                                editGrant: boxPane._edit_grant.get('value'),
                                addNodeGrant: boxPane._add_node_grant.get('value')
                            };

                            store.put(toUpdate).then(function(nitem) {
                                link = nitem;
                                setContents(boxPane);
                                mainPane[linkid].set('title',
                                                     link.linkName || 'Lista artykułów');
                                var okmsg = 'Zmiany zostały zapisane';
                                messagePane.set('content', okmsg);
                                setTimeout(function() {
                                    if (messagePane.get('content') === okmsg) {
                                        messagePane.set('content', '');
                                    }
                                }, 2000);
                            });
                        }
                        else {
                            messagePane.set('content', 'Akcja wstrzymana. Błędnie wypełniony formularz.');
                        }
                    }
                });

                messagePane = new ContentPane({
                    content: '',
                    region: 'center',
                    style: "margin: 0px 0px 11px 0px; padding: 4px 6px;"
                });

                var btnPane = new LayoutContainer({
                    region: 'bottom',
                    gutters: false,
                    style: "min-height: 34px; width: 100%"
                });

                btnPane.addChild(messagePane);
                btnPane.addChild(submit);

                mainPane[linkid].addChild(boxPane);
                mainPane[linkid].addChild(btnPane);
                panel.tabs.addChild(mainPane[linkid]);
            }
            panel.tabs.selectChild(mainPane[linkid]);
        });
    };

    return openPane;
});
