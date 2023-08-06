define([
    'dojo/_base/declare',
    'dijit/form/Select',
    'gtcms/stores/grants'
], function (
    declare, Select, grantsStore
) {
    return declare(
        [ Select ],
        {
            searchDelay: 100,
            labelAttr: 'name',
            store: grantsStore,
            maxHeight: 256,
            sortByLabel: false,
            _setInjectAttr: function (attr) {
                this._set('inject', attr);
                this._set('query', {inject: attr});
                this._set('store', grantsStore);
            }
        }
    );
});
