define([
    'dojo/_base/declare',
    'dijit/_Widget',
    'dijit/form/Select',
    'dojo/store/JsonRest'
],
function(
    declare, _Widget, FilteringSelect, Store
) {
    return declare(
        [FilteringSelect],
        {
            constructor: function(args, domNode) {
                args.searchDelay = 100;
                args.autoComplete =  false;
                args.hasDownArrow = false;
                args.valueAttr = "iso_code";
                args.nameAttr = "native_name";
                args.labelAttr = "native_name";
                args.store = new Store({target: '/_v1/languages/',
                                        idProperty: 'iso_code'});
            }
        });
});
