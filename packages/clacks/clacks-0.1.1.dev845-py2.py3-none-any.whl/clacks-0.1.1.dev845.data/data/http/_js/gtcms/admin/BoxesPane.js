define([
    'require',
    'dojo/_base/declare',
    "dojo/on",
    'dijit/layout/BorderContainer',
    'dijit/layout/ContentPane',
    'dijit/form/Button',
    'dijit/form/Select',
    'dijit/form/TextBox',
    'dijit/form/CheckBox',
    'dijit/ConfirmDialog',
    "dgrid/OnDemandGrid",
    "dgrid/Selection",
    "dgrid/Keyboard",
    "dgrid/extensions/DijitRegistry",
    "dgrid/extensions/ColumnResizer",
    "put-selector/put",
    'gtcms/admin/panel',
    'gtcms/dstores/boxes',
    // needed by template:
    './LanguageSelect'
], function (
    require, declare, on,
    BorderContainer, ContentPane, Button, Select, TextBox, CheckBox, ConfirmDialog,
    Grid, GridSelection, GridKeyboard, GridDijitRegistry, GridResizer,
    put, panel, store
) {
    var mainPane;

    var openPane = function () {
        var listGrid, filterField, gridTypeSelect;
        if (!mainPane) {
            mainPane = new BorderContainer({
                gutters: true,
                title: 'Artykuły',
                closable: true,
                onClose: function () {
                    mainPane = undefined;
                    return true;
                }
            });

            var applyFilters = function () {
            };

            filterField = new TextBox({intermediateChanges: true,
                                       onChange: applyFilters});

            var actionRenderCell = function (node, data, cell) {
                var box = put('div');
                on(put(box, 'a.dgrid-action', '✕', {'title': 'usuń'}),
                   'click', function () {
                       var dialog = new ConfirmDialog({
                           title: "Usuwanie artykułu",
                           content: "Czy na pewno?"
                       });
                       on(dialog.okButton,
                          'click', function(ev) {
                              store.remove(node.id);
                          });
                       dialog.show();
                   });
                on(put(box, 'a.dgrid-action', '✍', {'title':'edytuj'}),
                   'click', function () {
                       require(['./BoxPane'],
                               function(NodePane) {
                                   NodePane(node.id);
                               });
                   });

                return box;
            };

            var optionsPane = new ContentPane({
                style: 'height: auto; border-width: 0px; padding: 0px; margin: 5px 0px 0px;',
                region: 'top',
                content: '',
                postCreate: function () {
                    put(this.domNode, 'div[style=$]', 'float: left; padding: 0px 6px',
                        'Filtruj: ', filterField.domNode);
                }
            });

            var footerPane = new BorderContainer({
                style: 'height: 32px; margin: 0px 5px; border-width: 0px; text-align: right; padding: 0px;',
                region: 'bottom',
                gutters: false
            });

            var addBtn = new Button({
                label: 'Nowy artykuł',
                'region': 'center',
            });

            on(addBtn, 'click', function () {
                require(['./AddBoxDialog'], function (dialog) {
                    dialog.show(listGrid);//article.id, cGrid);
                });
            })


            listGrid = new declare([
                Grid,  GridSelection, GridResizer, GridKeyboard, GridDijitRegistry
            ])({
                pagingDelay: 100,
                columns: [
                    //{ field: 'position', label: "L.p.", reorderable: false },
                    { field: 'two-actions',
                      label: ' ',
                      sortable: false,
                      renderCell: actionRenderCell
                    },
                    {field: 'label', label: 'Etykieta'},
                    {field: 'title', label: 'Tytuł'},
                    {field: 'lang', label: 'Język'}
                ],
                collection: store.select(['id', 'label', 'title', 'lang'])
            });

            var gridListPane = new ContentPane({
                'class': "boxesGridHolder",
                style: "border: 0px; padding: 0px 5px;",
                region: 'center',
                content: listGrid.domNode
            });

            footerPane.addChild(addBtn);
            mainPane.addChild(optionsPane);
            mainPane.addChild(footerPane);
            mainPane.addChild(gridListPane);

            panel.tabs.addChild(mainPane);
        }
        panel.tabs.selectChild(mainPane);
    };

    panel.addMenuItem({
        label: 'Artykuły',
        section: 'Treści',
        priority: 90,
        onClick: openPane
    });

    panel.addUrlHandler('boxes', openPane);

    panel.addUrlHandler('box', function (oid) {
        require(['gtcms/admin/BoxPane'], function(OPane) {
            OPane(parseInt(oid));
        });
    });


    return { 'show': openPane };
});
