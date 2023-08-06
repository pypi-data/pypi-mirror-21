define([
    'dojo/_base/declare',
    'dstore/Rest',
    'dstore/Trackable'
    //"dstore/extensions/RqlQuery"
], function (
    declare, Rest, Trackable//, RqlQuery
) {
    return declare([Rest, Trackable], {
        target: '/_v1/user-grants/',
        sortParam: 'sort',
        useRangeHeaders: true
    })();
});
