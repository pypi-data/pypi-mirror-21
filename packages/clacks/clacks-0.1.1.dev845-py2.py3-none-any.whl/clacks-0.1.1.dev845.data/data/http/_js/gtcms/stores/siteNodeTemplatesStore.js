define([
    'dojo/store/Observable',
    'dojo/store/Cache',
    'dojo/store/JsonRest',
    'dojo/store/Memory'
],
function (
    Observable, CacheStore, JsonRestStore, Memory
) {
    return Observable(CacheStore(new JsonRestStore({
        target: '/_v1/site-node-templates/'
    }), new Memory({})));
});
