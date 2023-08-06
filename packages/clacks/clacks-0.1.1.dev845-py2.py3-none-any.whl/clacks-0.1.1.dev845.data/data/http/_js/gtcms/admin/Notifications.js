/*
 * Notifications.js
 */

define([
    'dojo/_base/declare',
    'dojo/store/JsonRest',
    'dijit/layout/BorderContainer',
    'dijit/layout/ContentPane',
    "dgrid/OnDemandGrid",
    "dgrid/Selection",
    "dgrid/Keyboard",
    "dgrid/extensions/DijitRegistry",
    "dgrid/extensions/ColumnResizer",
    'gtcms/admin/panel'
], function (
    declare, JsonRestStore,
    BorderContainer, ContentPane,
    Grid, GridSelection, GridKeyboard, GridDijitRegistry, GridResizer,
    panel
) {
    var mainPane;
    var grid;
    var refreshItems = function() {
        grid.set('store', undefined);
        grid.set('store', store);
        grid.set('query', {});
    };

    var store = new JsonRestStore({ target: '/_v1/user-notifications/' });

    var openPane = function () {

        if (!mainPane) {
            mainPane = new BorderContainer({
                design: 'sidebar',
                gutters: true,
                title: 'Komunikaty',
                closable: true,
                onClose: function () {
                    mainPane = undefined;
                    return true;
                }
            });

            grid = new (declare([Grid, GridDijitRegistry, GridSelection,
                GridResizer, GridKeyboard]))({
                    pagingDelay: 400,
                    columns: [
                        { field: 'position', label: 'L.p.', reorderable: false, sortable: false },
                        { field: 'id', label: 'Data', reorderable: false, sortable: false },
                        { field: 'type', label: 'Typ', reorderable: false, sortable: false },
                        { field: 'message', label: 'Komunikat', reorderable: false, sortable: false }
                    ]
                });


            refreshItems();

            var gridPane = new ContentPane({
                'class': 'notificationsGridTableHolder',
                style: 'padding: 0px; border: 0px;',
                region: 'center',
                content: grid.domNode
            });

            mainPane.addChild(gridPane);

            panel.tabs.addChild(mainPane);
        }
        panel.tabs.selectChild(mainPane);
    };

    return {'open': openPane, 'refresh': refreshItems};
});
