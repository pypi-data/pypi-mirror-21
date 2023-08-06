/*
 * ArticlePane.js
 */

define([
    'require',
    'dojo/_base/declare',
    'dojo/_base/array',
    'dojo/dom-geometry',
    'dojo/aspect',
    'dojo/on',
    'dojo/query',
    'put-selector/put',
    'dojo/when',
    'dijit/layout/ContentPane',
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    'dgrid/OnDemandGrid',
    'dgrid/Keyboard',
    'dgrid/extensions/DijitRegistry',
    'dgrid/extensions/DnD',
    'dijit/ConfirmDialog',
    'gtcms/admin/panel',
    'gtcms/dstores/siteNodes',
    'gtcms/stores/pageStyles',
    'gtcms/stores/pagePlacements',
    'gtcms/dstores/controls',
    'gtcms/LayoutTitlePane',
    'dojo/text!./templates/ArticlePane.html',
    //needed by template:
    'dijit/form/CheckBox',
    'dijit/form/TextBox',
    'dijit/form/Select',
    'dijit/form/Button',
    'dijit/form/ValidationTextBox',
    'dijit/layout/StackContainer',
    '/_ckeditor/ckeditor.js'
], function (
    require, declare, array, domGeom, aspect, on, query, put, when,
    ContentPane,
    _Templated, _WidgetsInTemplate,
    Grid, dgKeyboard, dgDijitRegistry, dgDnd,
    ConfirmDialog, panel,
    store, stylesStore, placementsStore, controlsStore,
    LayoutTitlePane, template
) {
    var mainPane = {};
    var openPane = function (articleid) {
        var ctrlPanes = {};
        when(store.get(articleid), function (article) {
            var main, cGrid;

            var renderActionCell = function (node, data, cell) {
                var box = put('div');
                if (!node.dynamic) {
                    put(box, 'a.dgrid-action.dgrid-action-disabled', '✕');
                }
                else {
                    on(put(box, 'a.dgrid-action', '✕', {'title': 'usuń'}),
                       'click', function () {
                           var dialog = new ConfirmDialog({
                               title: "Usuwanie elementu",
                               content: "Czy na pewno?"
                           });
                           on(dialog.okButton,
                              'click', function () {
                                  controlsStore.remove(node.id).then(function () {
                                      cGrid.refresh();
                                  });
                              });
                           dialog.show();
                       });
                }
                if (!node.editMode && (node._class !== 'article')) {
                    put(box, 'a.dgrid-action.dgrid-action-disabled', '✍');
                }
                else {
                    on(put(box, 'a.dgrid-action', '✍', {'title':'edytuj'}),
                       'click', function () {
                           if (node._class === 'article') {
                               main._formPane.selectChild(main._artPane);
                           }
                           else {
                               if (ctrlPanes[node.id] === undefined) {
                                   if (node.editMode === 'IFrame') {
                                       ctrlPanes[node.id] = new LayoutTitlePane({
                                           title: node.name,
                                           content: '<iframe src="/admin_control.php?id='+node.id+
                                                   '" style="width: 100%; height: 100%;'+
                                                   ' min-height: 400px; border-width: 0px;'+
                                                   ' margin: 0px;"></iframe>'
                                       });
                                       main._formPane.addChild(ctrlPanes[node.id]);
                                       main._formPane.selectChild(ctrlPanes[node.id]);
                                   }
                                   else if (node.editMode === 'ControlPane') {
                                       var pane = node._class[0].toUpperCase()+node._class.slice(1)+'Pane';
                                       require([
                                           './'+pane
                                       ], function (NodePane) {
                                           //repeated check is needed to prevent race condition:
                                           if (ctrlPanes[node.id] === undefined) {
                                               ctrlPanes[node.id] = new LayoutTitlePane({
                                                   title: node.name
                                               });
                                               var cPane = new NodePane({control: node});
                                               ctrlPanes[node.id].controlPane = cPane;
                                               ctrlPanes[node.id].addChild(cPane);

                                               main._formPane.addChild(ctrlPanes[node.id]);
                                           }
                                           main._formPane.selectChild(ctrlPanes[node.id]);
                                       });
                                   }
                               }
                               else {
                                   main._formPane.selectChild(ctrlPanes[node.id]);
                               }
                           }
                           return;
                       });
                }
                return box;
            };

            function titlePaneRealHeight(pane) {
                var height = 0, i;
                for (i=0; i<pane.domNode.children.length; i++) {
                    height += pane.domNode.children[i].clientHeight;
                }
                return height;
            }

            function _ckresize() {

                var editor = main.editor;
                if (editor && editor.instanceReady) {
                    var artSize = domGeom.getMarginBox(main._artPane.domNode);
                    var artTBarSize = domGeom.getMarginBox(main._artPane.domNode.children[0]);
                    editor.resize('100%',
                                  Math.max(300, artSize.h-artTBarSize.h-1));
                }
                else {
                    setTimeout( _ckresize, 100);
                }
            }

            function resize() {
                var nh;
                if (main._mainPane.domNode.offsetWidth < 840) {
                    if (main._topPane.region !== 'top' || main._propsPane.region !== 'top') {
                        main._topPane.region = 'top';
                        main._propsPane.region = 'top';
                        main._mainSplitter.region = 'top';
                        main._ctrlSplitter.region = 'top';
                        main._topPane.layout();
                        main._mainPane.layout();
                        cGrid.domNode.style.height = 'auto';
                        cGrid.domNode.style.maxHeight = '100px';
                        cGrid.domNode.style.minHeight = '100px';
                    }
                    nh = (titlePaneRealHeight(main._propsPane)+14+
                          titlePaneRealHeight(main._ctrlPane));
                    main._topPane.domNode.style.height = nh+'px';
                    main._propsPane.domNode.style.height = '';
                    main._ctrlPane.domNode.style.height = '';
                }
                else if (main._mainPane.domNode.offsetWidth < 1120) {
                    if (main._topPane.region !== 'top' || main._propsPane.region !== 'left') {
                        main._topPane.region = 'top';
                        main._propsPane.region = 'left';
                        main._ctrlSplitter.region = 'left';
                        main._mainSplitter.region = 'top';
                        main._topPane.layout();
                        main._mainPane.layout();
                        main._propsPane.set('open', main._propsPane.open || main._ctrlPane.open);
                        main._ctrlPane.set('open', main._propsPane.open || main._ctrlPane.open);
                        cGrid.domNode.style.height = (
                            query('.dijitTitlePaneContentInner',
                                  main._propsPane.domNode)[0].clientHeight+'px'
                        );
                        cGrid.domNode.style.maxHeight = '';
                    }
                    main._propsPane.domNode.style.width = '400px';
                    nh = Math.max(titlePaneRealHeight(main._propsPane),
                                  titlePaneRealHeight(main._ctrlPane));
                    main._propsPane.domNode.style.height = '';
                    main._ctrlPane.domNode.style.height = '';
                    main._topPane.domNode.style.height = (nh+3)+'px';
                }
                else {
                    if (main._topPane.region !== 'left' || main._propsPane.region !== 'top') {
                        main._topPane.region = 'left';
                        main._propsPane.region = 'top';
                        main._ctrlSplitter.region = 'top';
                        main._mainSplitter.region = 'left';
                        main._topPane.layout();
                        main._mainPane.layout();
                        main._propsPane.set('open', true);
                        main._ctrlPane.set('open', true);
                    }
                    main._topPane.domNode.style.width = '400px';
                    main._propsPane.domNode.style.width = '400px';
                    main._ctrlPane.domNode.style.width = '400px';
                    main._propsPane.domNode.style.height = '';
                    main._ctrlPane.domNode.style.height = '';
                    cGrid.domNode.style.height = Math.max(
                        64,
                        main._artPane.domNode.clientHeight-main._propsPane.domNode.clientHeight-32
                    )+'px';
                    cGrid.domNode.style.maxHeight = '';
                }
                _ckresize();
            }

            function layout() {
                // yes, its shitty workaround and better implementation is needed
                main._topPane.layout();
                main._mainPane.layout();
                resize();
                main._topPane.layout();
                main._mainPane.layout();
            }

            function propsToggle() {
                if ((main._mainPane.domNode.offsetWidth >= 840) &&
                    (main._mainPane.domNode.offsetWidth < 1120)) {
                    main._ctrlPane.set('open', !main._propsPane.open);
                }
                layout();
            }

            function ctrlToggle() {
                if ((main._mainPane.domNode.offsetWidth >= 840) &&
                    (main._mainPane.domNode.offsetWidth < 1120)) {
                    main._propsPane.set('open', !main._ctrlPane.open);
                }
                layout();
            }

            function setContents(pane) {
                pane._title.set('value', article.title);
                pane._linkName.set('value', article.linkName);
                pane._urlPart.set('value', article.urlPart);
                pane._visible.set('checked', article.visible);
                pane._isBase.set('checked', article.isBase);
                pane._noIndex.set('checked', article.noIndex);
                pane._targetUrl.href = article.url;
                pane._targetUrl.innerHTML = article.url;
                pane._placement.set('value', article.placement);
                pane._style.set('value', article.style);
            }

            function validateControls() {
                var response;
                for (var key in ctrlPanes) {
                    if (ctrlPanes.hasOwnProperty(key) &&
                        ctrlPanes[key].controlPane &&
                        ctrlPanes[key].controlPane.validate) {

                        response = ctrlPanes[key].controlPane.validate();
                        if (response) {
                            main.messagePane.set('content', response);
                            return false;
                        }
                    }
                }
                return true;
            }

            function submitControls() {
                var response = when(false);
                for (var key in ctrlPanes) {
                    if (ctrlPanes.hasOwnProperty(key) &&
                        ctrlPanes[key].controlPane &&
                        ctrlPanes[key].controlPane.submit) {
                        response = (function (response, key) {
                            return response.then(
                                function(result) {
                                    if (result) {
                                        main.messagePane.set('content', result);
                                        throw {error: 'Control submission failed',
                                               message: result};
                                    }
                                    else {
                                        return when(ctrlPanes[key].controlPane.submit())
                                    }

                                },
                                function() {
                                    main.messagePane.set('content', 'Control submission failed');
                                    throw {error: 'Control submission failed'};
                                });
                        })(response, key);
                    }
                }
                response = response.then(
                    function (response) {
                        if (response) {
                            main.messagePane.set('content', response);
                            throw {error: 'Control submission failed',
                                   message: response};
                        }
                        else {
                            return false;
                        }
                    },
                    function() {
                        main.messagePane.set('content', 'Control submission failed');
                        throw {error: 'Control submission failed',
                               message: response};
                    });

                return response;
            }

            if (!mainPane[articleid]) {
                main = mainPane[articleid] = declare([ContentPane, _Templated, _WidgetsInTemplate], {
                    templateString: template,
                    title: article.linkName || 'Artykuł',
                    closable: true,
                    article: article.body,
                    onClose: function () {
                        mainPane[articleid] = undefined;
                        return true;
                    },
                    resize: function () {
                        this.inherited(arguments);
                        this._mainPane.resize();
                    },
                    startup: function () {
                        this.inherited(arguments);
                        this._style.set('labelAttr', 'label');
                        this._style.set('sortByLabel', false);
                        this._style.set('query', {page: articleid});
                        this._style.set('store', stylesStore);
                        this._style.set('value', article.style);

                        this._placement.set('labelAttr', 'label');
                        this._placement.set('query', {page: articleid});
                        this._placement.set('store', placementsStore);
                        this._placement.set('value', article.style);

                        setContents(this);
                        this.editor = CKEDITOR.replace(
                            this._ckeditor,
                            {"width": "100%",
                             "height": "100%",
                             "contentsLanguage": article.lang,
                             "contentsCss": ("\/_css\/editor_body_"+
                                             (article.style || 'default')+
                                             ".css"),
                             "bodyClass": "editorBody"});

                        cGrid = declare([Grid, dgDijitRegistry, dgDnd, dgKeyboard])({
                            pagingDelay: 400,
                            minRowsPerPage: 100,
                            getBeforePut: false,
                            "class": "node-controls-grid",
                            collection: controlsStore.filter({sitenode: articleid}),
                            columns: [
                                { field:"two-actions",
                                  label: " ",
                                  sortable: false,
                                  renderCell: renderActionCell
                                },
                                { field: "name",
                                  label: "Nazwa",
                                  sortable: false
                                },
                                { field: "placement",
                                  label: "Miejsce",
                                  sortable: false
                                }
                            ]
                        });
                        main._ctrlPane.set('content', cGrid.domNode);
                        cGrid.domNode.style.margin='-11px';

                    },
                    postCreate: function () {
                        main = this;
                        this.inherited(arguments);
                        aspect.after(this._propsPane._wipeIn, 'onEnd', propsToggle);
                        aspect.after(this._propsPane._wipeOut, 'onEnd', propsToggle);
                        aspect.after(this._ctrlPane._wipeIn, 'onEnd', ctrlToggle);
                        aspect.after(this._ctrlPane._wipeOut, 'onEnd', ctrlToggle);
                        aspect.after(this._topPane, "resize", resize);
                    }
                })();


                on(main._addControl, 'click', function () {
                       require(['./AddControlDialog'], function (dialog) {
                           dialog.show(article.id, cGrid);
                       });
                });

                on(main._submit, 'click', function () {
                    if (main.form.validate() &&
                        validateControls()) {
                        main.messagePane.set('content', 'Zapisywanie zmian');

                        var toUpdate = {
                            id: articleid,
                            title: main._title.value,
                            linkName: main._linkName.value,
                            urlPart: main._urlPart.value,
                            visible: main._visible.checked,
                            isBase: main._isBase.checked,
                            noIndex: main._noIndex.checked,
                            placement: main._placement.value,
                            style: main._style.value
                        };
                        if (main.editor.checkDirty()) {
                            toUpdate.body = main.editor.getData();
                            main.editor.resetDirty();
                        }
                        store.put(toUpdate).then(function (nitem) {
                            article = nitem;
                            setContents(main);
                            main.set('title', article.linkName || 'Artykuł');
                        }).then(submitControls).then(function() {
                            var okmsg = 'Zmiany zostały zapisane';
                            main.messagePane.set('content', okmsg);
                            setTimeout(function () {
                                if (main.messagePane &&
                                    (main.messagePane.get('content') === okmsg)) {
                                    main.messagePane.set('content', '');
                                }
                            }, 2000);
                        })
                    }
                    else {
                        main.messagePane.set('content', 'Akcja wstrzymana. Błędnie wypełniony formularz.');
                    }
                });

                panel.tabs.addChild(mainPane[articleid]);
            }
            panel.tabs.selectChild(mainPane[articleid]);
        });
    };

    return openPane;
});
