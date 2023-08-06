define([
    'dojo/store/Observable',
    'dojo/store/JsonRest'
], function (
    Observable, JsonRest
) {
    return new Observable(new JsonRest({ target: '/_v1/user-stats/daily-logins/',
                                         sortParam: 'sort' }));
});
