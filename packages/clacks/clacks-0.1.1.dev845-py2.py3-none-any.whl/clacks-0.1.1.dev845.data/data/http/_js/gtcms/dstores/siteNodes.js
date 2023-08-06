define([
    'dojo/_base/declare',
    'dstore/Rest',
    'dstore/Trackable'
    //"dstore/extensions/RqlQuery"
], function (
    declare, Rest, Trackable//, RqlQuery
) {
    return declare([Rest, Trackable /*,RqlQuery*/], {
		constructor: function () {
			this.root = this;
		},
		mayHaveChildren: function (object) {
			return object.childNodesCount>0;
		},
		getRootCollection: function () {
			return this.root.filter({ parent: 'head' });
		},

		getChildren: function (object) {
			return this.root.filter({ parent: this.getIdentity(object) });
		}
    })({
        target: '/_v1/site-nodes/',
        useRangeHeaders: true,
        defaultNewToStart: true
    });
});
