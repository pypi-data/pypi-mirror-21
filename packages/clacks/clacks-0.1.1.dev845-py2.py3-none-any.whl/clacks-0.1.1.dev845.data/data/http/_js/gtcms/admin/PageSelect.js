define([
    'dojo/_base/declare',
    'dijit/_Widget',
    'dijit/form/FilteringSelect',
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
                args.searchAttr = "linkName";
                args.labelAttr = "fullName";
                args.query = {'type': 'page'};
                args.store = new Store({target: '/_v1/pages-filter/'});
            },
            buildRendering: function() {
                this.inherited(arguments);
            },
            startup: function() {
                this.inherited(arguments);
            }
        });
});
