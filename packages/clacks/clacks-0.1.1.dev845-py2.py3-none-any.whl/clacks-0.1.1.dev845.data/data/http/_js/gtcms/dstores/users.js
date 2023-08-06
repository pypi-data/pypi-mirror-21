define([
    'dojo/_base/declare',
    'dstore/Rest',
    'dstore/Trackable'
    //"dstore/extensions/RqlQuery"
], function (
    declare, Rest, Trackable//, RqlQuery
) {
    return  declare([Rest, Trackable], {
		constructor: function () {
			this.root = this;
		},
        mayHaveChildren: function(parent) {
            return parent.hasChildren>0;
        },
		getRootCollection: function () {
			return this.root.filter({ parent: '' });
		},
        getChildren: function(parent, options) {
		    return this.root.filter({parent: parent.id});
	    }
    })({
        target: '/_v1/users/',
        sortParam: 'sort',
        useRangeHeaders: true
    });
});
