/*
 * LinkPane.js
 */

define([
    'dojo/_base/declare',
    'dojo/on',
    'dojo/dom-style',
    'dojo/when',
    'dijit/layout/BorderContainer',
    'dijit/layout/ContentPane',
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    'dijit/form/Button',
    'gtcms/admin/panel',
    'gtcms/stores/siteNodes',
    'gtcms/stores/pagePlacements',
    'dojo/text!../templates/LinkPane.html',
    //needed by template:
    'dijit/TitlePane',
    'dijit/form/TextBox',
    'dijit/form/RadioButton',
    'dijit/form/Select',
    'gtcms/admin/PageSelect'
], function (
    declare, on, domStyle, when,
    BorderContainer, ContentPane,
    _Templated, _WidgetsInTemplate, Button,
    panel, store, placementsStore,
    template
) {
    var mainPane = {};
    var openPane = function (linkid) {
        when(store.get(linkid), function (link) {

            var messagePane, boxPane;

            function setExternalLinkMode(pane) {
                domStyle.set(pane._localLinkSelect, 'display',
                             pane._localLinkRadio.checked ? null: 'none');
                domStyle.set(pane._remoteLinkSelect, 'display',
                             pane._remoteLinkRadio.checked ? null: 'none');
                pane._localLinkTarget.set('disabled',
                                          !pane._localLinkRadio.checked);
                pane._remoteLinkTarget.set('disabled',
                                           !pane._remoteLinkRadio.checked);
                }

            if (!mainPane[linkid]) {
                mainPane[linkid] = new BorderContainer({
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
                    pane._placement.set('value', link.placement);
                    pane._visible.set('checked', link.visible);
                    pane._localLinkTarget.set('value', link._page);
                    pane[(link._page>0 || !link.externalLink || link.externalLink.length === 0 ?
                          '_local' : '_remote')+'LinkRadio'].set('checked', true);
                    pane._remoteLinkTarget.set('value', link.externalLink);
                    domStyle.set(pane._localLinkSelect, 'display', pane._localLinkRadio.checked ? null: 'none');
                    domStyle.set(pane._remoteLinkSelect, 'display', pane._remoteLinkRadio.checked ? null: 'none');
                    setExternalLinkMode(pane);
                };

                boxPane = new declare([ContentPane, _Templated, _WidgetsInTemplate], {
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
                        on(this._remoteLinkRadio, 'change', function() {
                            setExternalLinkMode(boxPane);
                        });

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
                            var toUpdate = { id: linkid,
                                             externalLink: (boxPane._remoteLinkRadio.checked ?
                                                            boxPane._remoteLinkTarget.get('value') : ''),
                                             _page: (boxPane._localLinkRadio.checked ?
                                                     parseInt(boxPane._localLinkTarget.get('value'), 10) : null),
                                             linkName: boxPane._linkName.get('value'),
                                             visible: boxPane._visible.checked,
                                             placement: boxPane._placement.get('value')
                                           };

                            store.put(toUpdate).then(function(nitem) {
                                link = nitem;
                                setContents(boxPane);
                                mainPane[linkid].set('title', link.linkName || 'Link');
                                messagePane.set('content', 'Zmiany zostały zapisane');
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

                var btnPane = new BorderContainer({
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
