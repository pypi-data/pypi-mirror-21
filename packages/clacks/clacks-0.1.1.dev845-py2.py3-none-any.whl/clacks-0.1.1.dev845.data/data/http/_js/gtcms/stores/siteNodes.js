define([
    'dojo/_base/declare',
    'dojo/store/Observable',
    'dojo/store/Cache',
    'dojo/store/JsonRest',
    'dojo/store/Memory',
    "dojo/store/util/SimpleQueryEngine"
],
function (
    declare, Observable, CacheStore,
    JsonRestStore, Memory, SimpleQueryEngine
) {
    return Observable(new declare([JsonRestStore], {
        getChildren: function(parent, options) {
            return this.query({parent: parent.id}, options);
        },
        mayHaveChildren: function(parent) {
            return parent.childNodesCount>0;
        },
        put: function(object, options) {
            if (this.parentProperty && options && options.parent !== undefined) {
                object[this.parentProperty] = options.parent;
            }
            if (this.nextSiblingProperty && options && options.before !== undefined) {
                object[this.nextSiblingProperty] = options.before;
            }
            return this.inherited(arguments);
        },
        queryEngine: SimpleQueryEngine
    })({
        target: '/_v1/site-nodes/',
        parentProperty: '_parent',
        nextSiblingProperty: '_nextSibling'
    }));
});
