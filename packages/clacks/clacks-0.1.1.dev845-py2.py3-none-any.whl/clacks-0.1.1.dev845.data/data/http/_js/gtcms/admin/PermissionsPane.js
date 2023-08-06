/*
 * PermissionsPane.js
 */

define([
    'dojo/_base/declare',
    'dojo/aspect',
    'dojo/on',
    'dojo/query',
    'put-selector/put',
    'dijit/layout/ContentPane',
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    'dgrid/OnDemandGrid',
    'dgrid/Selection',
    'dgrid/Keyboard',
    'dgrid/Editor',
    "dgrid/extensions/DijitRegistry",
    'gtcms/admin/panel',
    'gtcms/dstores/grants',
    'gtcms/dstores/user-grants',
    'dijit/form/CheckBox',
    'dojo/text!../templates/PermissionsPane.html',
    //needed by template:
    'dijit/TitlePane'
], function (
    declare, aspect, on, query, put,
    ContentPane,
    _Templated, _WidgetsInTemplate,
    Grid, GridSelection, dgKeyboard, GridEditor, dgDijitRegistry,
    panel,
    store, userGrantStore, CheckBox,
    template
) {
    function _(arg) {
        return arg;
    }

    var main;

    var openPane = function () {
        var pGrid, gGrid, uGrid, ustore;

        if (!main) {
            main = declare([ContentPane, _Templated, _WidgetsInTemplate], {
                templateString: template,
                title: _("Uprawnienia"),
                closable: true,
                onClose: function () {
                    main = undefined;
                    return true;
                },
                resize: function () {
                    this.inherited(arguments);
                },
                startup: function () {
                    this.inherited(arguments);
                    var currentGrant;

                    pGrid = declare([Grid, GridSelection, dgDijitRegistry, dgKeyboard])({
                        pagingDelay: 400,
                        minRowsPerPage: 100,
                        getBeforePut: false,
                        collection: store,
                        columns: [
                            {
                                field: "one-action",
                                label: " ",
                                sortable: false,
                                style: "width: 80px"
                            },
                            {
                                field: "id",
                                label: "Nazwa",
                                sortable: false
                            }
                        ]
                    });
                    main._permissionsPane.set('content', pGrid.domNode);
                    pGrid.domNode.style.margin = '-11px';

                    gGrid = declare([Grid, dgDijitRegistry, dgKeyboard])({
                        pagingDelay: 400,
                        "class": "permissions-group-grants",
                        keepScrollPosition: true,
                        minRowsPerPage: 100,
                        selectionMode: 'single',
                        getBeforePut: false,
                        collection: null,
                        columns: [
                            {
                                field: "granted",
                                label: " ",
                                sortable: false,
                                renderCell: function(data, value, node, options) {
                                    node.widget = CheckBox();
                                    if (currentGrant===currentGrant.toUpperCase() &&
                                        currentGrant!==currentGrant.toLowerCase() &&
                                        currentGrant !== 'AUTHORIZED') {

                                        node.widget.set('disabled', true);
                                    }
                                    if (currentGrant===data.id ||
                                        data.id==='AUTHORIZED') {
                                        node.widget.set('disabled', true);
                                    }
                                    if (data.granted_by[currentGrant]) {
                                        node.widget.set('checked', true);
                                    }
                                    on(node.widget, 'change', function(newval) {
                                        var granted_by={};
                                        if ((!data.granted_by[currentGrant])===newval) {
                                            granted_by[currentGrant] = newval;
                                            store.put({
                                                'id': data.id,
                                                'granted_by': granted_by
                                            });
                                        }
                                    });
                                    //elem.startup();
                                    return node.widget.domNode;
                                }

                            },
                            {
                                field: "id",
                                label: "Nazwa",
                                sortable: false
                            }
                        ]
                    });
                    aspect.before(gGrid, "removeRow", function(row) {
                        var cell = gGrid.cell(row, '0').element;
                        var widget = (cell.contents || cell).widget;
                        if (widget){ widget.destroyRecursive(); }
                    })
                    main._grantedPane.set('content', gGrid.domNode);
                    gGrid.domNode.style.margin = '-11px';

                    on(pGrid, 'dgrid-select', function(event) {
                        currentGrant = event.rows[0].data.id;
                        gGrid.set('collection', store.filter({'granted_by': currentGrant}));
                        uGrid.set('collection', userGrantStore.filter({'grant': currentGrant}));
                    });

                    uGrid = declare([Grid, GridEditor, dgDijitRegistry, dgKeyboard])({
                        "class": "permissions-user-grants",
                        pagingDelay: 400,
                        minRowsPerPage: 100,
                        getBeforePut: false,
                        keepScrollPosition: true,
                        columns: [
                            {
                                field: "directly",
                                label: " ",
                                sortable: false,
                                editor: CheckBox,
                                autoSave: true
                            },
                            {
                                field: "implicit",
                                label: " ",
                                sortable: false,
                                renderCell: function (node, data, cell) {
                                    if (node.granted) {
                                        return put('span', '✓');
                                    }
                                }
                            },
                            { field: "login", label: "Login", sortable: false}
                        ]
                    });
                    main._usersPane.set('content', uGrid.domNode);
                    uGrid.domNode.style.margin = '-11px';
                },
                postCreate: function () {
                    this.inherited(arguments);
                }
            })();

            panel.tabs.addChild(main);
        }
        panel.tabs.selectChild(main);
    };


    panel.addMenuItem({
        label: _('Uprawnienia'),
        section: _('Ustawienia'),
        priority: 60,
        onClick: openPane
    });

    panel.addUrlHandler('permissions', openPane);

    return {'show': openPane};
});
