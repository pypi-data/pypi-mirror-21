define([
    'dojo/_base/declare',
    'dstore/Rest',
    'dstore/Trackable'
], function (
    declare, Rest, Trackable
) {
    return declare([Rest, Trackable])({
        target: '/_v1/controls/',
        useRangeHeaders: true
    });
});
