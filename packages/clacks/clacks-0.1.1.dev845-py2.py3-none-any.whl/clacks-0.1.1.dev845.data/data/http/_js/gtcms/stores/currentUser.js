define([
        'dojo/store/Observable',
        'dojo/store/Cache',
        'dojo/store/JsonRest',
        'dojo/store/Memory'
],
function (Observable, CacheStore,
          JsonRestStore, Memory) {
    var cache = new Observable(new Memory({}));
    var result = new Observable(
        CacheStore(new JsonRestStore({ target: '/_rest/user/current/' }),
                   cache));
    result.cache = cache;
    return result;
});
