/*
 * UsersList.js
 */

define([
    'dojo',
    'dojo/_base/declare',
    'dojo/aspect',
    'dijit/layout/BorderContainer',
    'dijit/layout/ContentPane',
    'dijit/form/Button',
    'dijit/form/Select',
    'dijit/form/TextBox',
    'dijit/form/CheckBox',
    "dgrid/OnDemandGrid",
    "dgrid/Selection",
    "dgrid/Keyboard",
    "dgrid/Tree",
    "dgrid/extensions/DijitRegistry",
    "dgrid/extensions/ColumnHider",
    "dgrid/extensions/ColumnReorder",
    "dgrid/extensions/ColumnResizer",
    'gtcms/dgrid/IndexColumn',
    "put-selector/put",
    'gtcms/admin/panel',
    'gtcms/dstores/users',
    //"xstyle/css!/_css/admin/shop.css",
    "xstyle/css!/_js/dgrid/css/skins/claro.css"
], function (
    dojo, declare, aspect,
    BorderContainer, ContentPane, Button, Select, TextBox, CheckBox,
    Grid, GridSelection, GridKeyboard, GridTree,
    GridDijitRegistry, GridHider, GridReorder, GridResizer, IndexColumn,
    put, panel, store
) {
    var mainPane;

    function _(a) { return a; }

    var openPane = function () {

        var listGrid, treeGrid, filterField, gridTypeSelect;

        function colorizeRow(row, args) {
            if (args[0].role && /^[a-z]+$/i.test(args[0].role)) {
                put(row, '.user-role-'+args[0].role);
            }
            return row;
        }

        if (!mainPane) {
            mainPane = new BorderContainer({
                design: 'sidebar',
                gutters: true,
                title: _('Użytkownicy'),
                closable: true,
                onClose: function () {
                    mainPane = undefined;
                    return true;
                }
            });

            var applyFilters = function () {
                listGrid.set('collection',
                             store.filter({ filter: '*'+filterField.value+'*' }));
                /* disabled until implemented
                   moreover it should be implemented in a way that
                   only query for visible view is executed
                  treeGrid.set('query',
                    { filter: '*'+filterField.value+'*' });
                */
            };

            var switchView = function () {
                //should be implemented as switching panes...
                if (gridTypeSelect.value=='tree') {
                    mainPane.removeChild(gridListPane);
                    mainPane.addChild(gridTreePane);
                }
                else {
                    mainPane.removeChild(gridTreePane);
                    mainPane.addChild(gridListPane);
                }
            };


            filterField = new TextBox({intermediateChanges: true,
                onChange: applyFilters});

            gridTypeSelect = new Select({options: [{label: 'lista', value: 'list'},
                                                   {label: 'drzewo', value: 'tree'}],
                                        style: 'width: 64px;',
                                        onChange: switchView});

            var optionsPane = new ContentPane({
                style: 'height: auto; border-width: 0px; padding: 0px; margin: 2px 0px 0px 0px;',
                region: 'top',
                content: '',
                postCreate: function () {
                    put(this.domNode, 'div[style=$]', 'float: left; padding: 0px 1px',
                        'Filtr: ', filterField.domNode);
                    put(this.domNode, 'div[style=$]', 'float: right; padding: 0px 0px',
                        'Widok: ', gridTypeSelect.domNode);
                }
            });

            var footerPane = new BorderContainer({
                style: 'height: 27px; margin: 0px 0px; border-width: 0px; text-align: right; padding: 0px;',
                region: 'bottom',
                gutters: false
            });

            var addBtn = new Button({
                label: _('Dodaj użytkownika'),
                'region': 'center',
                onClick: function() {
                    require(['gtcms/admin/UserProfilePane'], function(UPP) {
                        UPP.show('new');
                    });
                }
            });

            listGrid = new (declare([
                Grid, GridDijitRegistry, GridSelection,
                GridReorder, GridResizer,
                GridKeyboard, GridHider]))({
                    pagingDelay: 400,
                    columns: [
                        IndexColumn({field: 'idx', label: ''}),
                        { field: 'login', label: _('Login') },
                        { field: 'fullName', label: _('Użytkownik') },
                        { field: 'company', label: _('Firma') },
                        { field: 'walletAmount', label: _('Saldo') },
                        { field: 'created', label: _('Utworzono') },
                        { field: 'active', label: _('Aktywny'),
                          get: function(item) {
                              return item.active ? '✓' : '';
                          }
                        },
                        { field: 'lastLogin', label: _('Logowanie') },
                        { field: 'role', label: _('Funkcja') }
                    ],
                    "class": "usersList",
                    collection: store
                });

            treeGrid = new (declare([Grid, GridTree, GridDijitRegistry, GridSelection,
                GridReorder, GridResizer,
                GridKeyboard, GridHider]))({
                    pagingDelay: 400,
                    columns: [
                        { field: 'fullName', label: _('Klient'), renderExpando: true, allowDuplicates: true },
                        { field: 'login', label: _('Login'), allowDuplicates: true },
                        { field: 'company', label: _('Firma') },
                        { field: 'walletAmount', label: _('Punkty') },
                        { field: 'created', label: _('Utworzono') },
                        { field: 'active', label: _('Aktywny'),
                          get: function(item) {
                              return item.active ? '✓' : '';
                          }
                        },
                        { field: 'lastLogin', label: 'Logowanie' },
                        { field: 'role', label: 'Funkcja' }
                    ],
                    "class": "usersList",
                    collection: store.getRootCollection()
                });

            aspect.after(listGrid, "renderRow", colorizeRow);
            aspect.after(treeGrid, "renderRow", colorizeRow);

            listGrid.on(".dgrid-row:dblclick", function (evt) {
                var row = listGrid.row(evt);
                require(['gtcms/admin/UserProfilePane'], function (UPP) {
                    UPP.show(row.data.id);
                });
            });


            treeGrid.on(".dgrid-row:dblclick", function (evt) {
                var row = treeGrid.row(evt);
                require(['gtcms/admin/UserProfilePane'], function (UPP) {
                    UPP.show(row.data.id);
                });
            });

            var gridListPane = new ContentPane({
                'class': "usersGridHolder",
                style: "border: 0px; padding: 0px 0px;",
                region: 'center',
                content: listGrid.domNode
            });

            var gridTreePane = new ContentPane({
               'class': "usersGridHolder",
                style: "border: 0px; padding: 0px 5px;",
                region: 'center',
                content: treeGrid.domNode
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
        label: _('Użytkownicy'),
        section: _('Ustawienia'),
        priority: 90,
        onClick: openPane
    });

    panel.addUrlHandler('users', openPane);

    return { 'show': openPane };
});
