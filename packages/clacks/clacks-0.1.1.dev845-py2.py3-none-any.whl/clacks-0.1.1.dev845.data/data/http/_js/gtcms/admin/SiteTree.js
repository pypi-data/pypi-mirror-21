/* dgrid based version of site structure management */

define([
    'require',
    'dojo/_base/declare',
    "dojo/when",
    "dojo/on",
    "dojo/aspect",
    'put-selector/put',
    'dijit/layout/BorderContainer',
    'dijit/layout/ContentPane',
    'dijit/form/Button',
    'dijit/ConfirmDialog',
    'dgrid/OnDemandGrid',
    'dgrid/Tree',
    'dgrid/Keyboard',
    'dgrid/Selection',
    'dgrid/extensions/ColumnHider',
    'dgrid/extensions/ColumnReorder',
    'dgrid/extensions/ColumnResizer',
    "dgrid/extensions/DijitRegistry",
    "dgrid/extensions/DnD",
    "gtcms/dstores/siteNodes",
    'gtcms/admin/panel'
], function (
    require, declare, when, on, aspect, put,
    BorderContainer, ContentPane, Button, ConfirmDialog,
    Grid, GridTree, dgKeyboard, dgSelection, dgColumnHider, dgColumnReorder,
    dgColumnResizer, dgDijitRegistry, dgDnD, store, panel
) {
    var mainPane;
    var tree;
    var cacheid = 'admin.sitetree.expansion_state';
    var expanded_rows = localStorage[cacheid] ? JSON.parse(localStorage[cacheid]) : {};
    var openPane = function () {
        if (!mainPane) {

            mainPane = new BorderContainer({
                design: 'sidebar',
                gutters: true,
                title: 'Struktura',
                closable: true,
                onClose: function () {
                    mainPane = undefined;
                    return true;
                }
            });

            var actionRenderCell = function (node, data, cell) {
                var box = put('div');
                if (node.childNodesCount || !node.editGranted) {
                    put(box, 'a.dgrid-action.dgrid-action-disabled', '✕');
                }
                else {
                    on(put(box, 'a.dgrid-action', '✕', {'title': 'usuń'}),
                       'click', function () {
                           var dialog = new ConfirmDialog({
                               title: "Usuwanie pozycji struktury",
                               content: "Czy na pewno?"
                           });
                           on(dialog.okButton,
                              'click', function(ev) {
                                  console.log(node);
                                  store.remove(node.id).then(function() {
                                      store.get(node._parent);
                                  });
                                  //tree.refresh();
                              });
                           dialog.show();
                       });
                }
                if (node.addNodeGranted) {
                    on(put(box, 'a.dgrid-action', '↴', {'title':'dodaj podstronę'}),
                       'click', function (event) {
                           console.log([node, data, cell]);
                           require(['./AddSiteNodeDialog'], function(dialog) {
                               dialog.show(node.id);
                           });
                       });
                }
                else {
                    put(box, 'a.dgrid-action.dgrid-action-disabled', '↴');
                }
                if (node.editGranted) {
                    /*on(put(box, 'div.dgrid-action', '⎘'),
                         'click', function () {
                           new Dialog({
                               title: "Kopiowanie artykułu",
                               content: "W trakcie implementacji.",
                               style: "width: 200px"
                           }).show();
                       });*/
                    on(put(box, 'a.dgrid-action', '✍', {'title':'edytuj'}),
                       'click', function () {
                           var pane = node.type[0].toUpperCase()+node.type.slice(1)+'Pane';
                           require(['./'+pane],
                                   function(NodePane) {
                                       NodePane(node.id);
                                   });
                       });
                }
                else {
                    put(box, 'a.dgrid-action.dgrid-action-disabled', '✍');
                }
                return box;
            };

            tree = new declare([
                Grid, GridTree, dgDijitRegistry, dgKeyboard, dgSelection, dgDnD
            ])({
                pagingDelay: 400,
                minRowsPerPage: 100,
                maxRowsPerPage: 250,
                orderColumn: 'position',
                columns: [
                    { field: 'three-actions',
                      label: ' ',
                      sortable: false,
                      renderCell: actionRenderCell
                    },
                    { label: 'Nazwa linku',
                      field: 'linkName',
                      sortable: false,
                      renderExpando: true
                    },
                    { field: 'visible',
                      label: '👀',
                      sortable:false,
                      get: function(row) {
                          return row.visible ? '✓' : '';
                      }
                    },
                    { field: "type", label: "Typ", sortable: false,
                      renderCell: function(data, value, node, options) {
                          return put('a[title=$]',
                                     value,
                                     {'article': '🖺',
                                      'articlelist': '📂',
                                      'meta': '🗋',
                                      'link':'🔗',
                                      'section': '📦'}[value] || '?'
                                    );
                      }
                    },
                    { field: "placement", label: "Linkowanie", sortable: false }
                ],
                selectionMode: 'single',
                getBeforePut: false,
                collection: store.getRootCollection(),
                shouldExpand: function(row, level, previouslyExpanded) {
                    var result = false;
                    if (previouslyExpanded!==undefined) {
                        result = previouslyExpanded;
                    }
                    if (expanded_rows[row.id] !== undefined) {
                        result = expanded_rows[row.id];
                    }
                    return result;
                },
                enableTreeTransitions: false,
				dndParams: {
					allowNested: true, // also pick up indirect children w/ dojoDndItem class
					checkAcceptance: function(source, nodes) {
                        //console.log([source, nodes]);
                        return true;
						//return source !== this; // Don't self-accept.
					},
                    onDropInternal: function (nodes, copy) {
                        this.inherited(arguments);
                        var grid = this.grid, targetRow, targetPosition;

                        if (!this._targetAnchor) {
                            return;
                        }

                        targetRow = grid.row(this._targetAnchor);
                        targetPosition = parseInt(targetRow.data[grid.orderColumn]);
                        responses = 1;

                        nodes.forEach(function (node, idx) {
                            targetPosition += idx;
                            var object = {id:grid.row(node).id};
                            object[grid.orderColumn] = targetPosition;
                            store.put(object).then( function () {
                                if (responses == nodes.length) {
                                    grid.refresh();
                                }
                                else {
                                    responses++;
                                }
                            });
                        });
                    }
                }
            });
            aspect.before(tree, 'expand', function(row, state) {
                if (row.data!==undefined) {
                    if ((state!==undefined) ? !!state : !expanded_rows[row.id]) {
                        expanded_rows[row.id] = true;
                    }
                    else {
                        delete expanded_rows[row.id];
                    }
                    localStorage[cacheid] = JSON.stringify(expanded_rows);
                }
            });

            var treePane = new ContentPane({
                'class': "siteTreeHolder",
                style: "padding: 5px 5px; border: 0px;",
                region: 'center',
                content: tree.domNode
            });

            mainPane.addChild(treePane);
            panel.tabs.addChild(mainPane);
        }
        panel.tabs.selectChild(mainPane);
    };

    panel.addMenuItem({
        label: 'Struktura',
        priority: 20,
        onClick: openPane
    });

    panel.addUrlHandler('tree', openPane);

    panel.addUrlHandler('site-node', function (nodeid) {
        when(store.get(nodeid), function (node) {
            var pane = node.type[0].toUpperCase()+node.type.slice(1)+'Pane';
            require(['gtcms/admin/'+pane], function(NodePane) {
                NodePane(parseInt(nodeid));
            });
        });
    });

    return {'show': openPane,

            'refresh': function() {
            // calling this function is hopefully temporary workaround
            // until proper implementation of Observable on siteTree will be done
                if (tree) {
                    tree.refresh();
                }
            }
           };
});
