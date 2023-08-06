/*
 * ArticlePane.js
 */

define([
    'require',
    'dojo/_base/declare',
    'dojo/dom-geometry',
    'dojo/aspect',
    'dojo/on',
    'put-selector/put',
    'dijit/layout/ContentPane',
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    'dgrid/OnDemandGrid',
    'dgrid/Keyboard',
    'dgrid/extensions/DijitRegistry',
    'dgrid/extensions/DnD',
    'dijit/ConfirmDialog',
    './panel',
    '../dstores/boxes',
    '../LayoutTitlePane',
    'dojo/text!./templates/BoxPane.html',
    //needed by template:
    'dijit/form/Form',
    'dijit/form/Button',
    'dijit/form/TextBox',
    'dijit/form/ValidationTextBox',
    'dijit/layout/StackContainer',
    '/_ckeditor/ckeditor.js'
], function (
    require, declare, domGeom, aspect, on, put,
    ContentPane,
    _Templated, _WidgetsInTemplate,
    Grid, dgKeyboard, dgDijitRegistry, dgDnd,
    ConfirmDialog, panel,
    store,
    LayoutTitlePane, template
) {
    var mainPane = {};
    var openPane = function (boxid) {
        store.get(boxid).then(function (box) {
            var main;

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
                main._mainPane.layout();
                _ckresize();
            }

            function layout() {
                // yes, its shitty workaround and better implementation is needed
                main._mainPane.layout();
                resize();
                main._mainPane.layout();
            }

            function propsToggle() {
                layout();
            }

            function setContents(pane) {
                pane._title.set('value', box.title);
                pane._label.set('value', box.label);
            }

            if (!mainPane[boxid]) {
                main = mainPane[boxid] = declare([ContentPane, _Templated, _WidgetsInTemplate], {
                    templateString: template,
                    title: box.label || 'Artykuł',
                    closable: true,
                    _content: box.content,
                    onClose: function () {
                        mainPane[boxid] = undefined;
                        return true;
                    },
                    resize: function () {
                        this.inherited(arguments);
                        //this._mainPane.resize();
                    },
                    startup: function () {
                        this.inherited(arguments);

                        setContents(this);
                        this.editor = CKEDITOR.replace(
                            this._ckeditor,
                            {"width": "100%",
                             "height": "100%",
                             "contentsLanguage": box.lang,
                             "contentsCss": "/_css/box_contents.css",
                             "bodyClass": "editorBody"});
                    },
                    postCreate: function () {
                        main = this;
                        this.inherited(arguments);
                        aspect.after(this._propsPane._wipeIn, 'onEnd', propsToggle);
                        aspect.after(this._propsPane._wipeOut, 'onEnd', propsToggle);
                        aspect.after(this._artPane, "resize", _ckresize);
                    }
                })();

                on(main._submit, 'click', function () {
                    if (main.form.validate()) {
                        main.messagePane.set('content', 'Zapisywanie zmian');

                        var toUpdate = {
                            id: boxid,
                            title: main._title.get('value'),
                            label: main._label.get('value')
                        };
                        if (main.editor.checkDirty()) {
                            toUpdate.content = main.editor.getData();
                            main.editor.resetDirty();
                        }
                        store.put(toUpdate).then(function (nitem) {
                            box = nitem;
                            setContents(main);
                            main.set('title', box.label || 'Artykuł');
                        }).then(function() {
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

                panel.tabs.addChild(mainPane[boxid]);
            }
            panel.tabs.selectChild(mainPane[boxid]);
        });
    };

    return openPane;
});
