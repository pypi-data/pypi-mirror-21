/**
 * session module is responsible for checking user status
 * and authorizing him to the application
 */
define([
    'dojo/_base/xhr'
], function (
    xhr
) {
    var CHECK_INTERVAL = 300000; //authorization cache validity (5 mins)
    var _authorized;
    var _lastCheck = (new Date(0));

    var _setAuthorized = function (newAuth) {
        _authorized = newAuth;
        _lastCheck = (new Date());
        return _authorized; //for chaining
    };

    var logoutFn = function () {
        return xhr.post({
            url: "/_v1/session/logout/",
            handleAs: 'json'
        }).then(_setAuthorized);
    };

    return {
        logout: logoutFn,

        login: function (login, password) {

            return xhr.post({
                url: "/_v1/session/login/",
                content: {login: login,
                          password: password},
                handleAs: 'json'
            }).then(_setAuthorized);
        },
        granted: function (grantName) {
            return (_authorized &&
                    _authorized.grants &&
                    ((_authorized.grants.indexOf(grantName) != -1) ||
                     (_authorized.grants.indexOf('SITE_ADMIN') != -1)));
        },
        // Returns last checked user's status as an array, or as a promise if
        // forceRefresh parameter is set to true.
        // refreshes status in a background every CHECK_INTERVAL time
        status: function(forceRefresh) {
            if (forceRefresh || (((new Date()) - _lastCheck) > CHECK_INTERVAL)) {
                var dresponse = xhr.post({
                    url: "/_v1/session/status/",
                    handleAs: 'json'
                }).then(_setAuthorized,
                        function (errorcode) {
                            console.log(errorcode);
                        });
                if (forceRefresh) {
                    return dresponse;
                }
            }
            return _authorized;
        }
    };
});
