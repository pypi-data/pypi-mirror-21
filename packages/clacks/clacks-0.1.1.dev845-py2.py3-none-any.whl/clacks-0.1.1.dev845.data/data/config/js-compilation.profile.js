var profile = (function(){
    return {
        basePath: "../http/_js",
        releaseDir: "./.minified",
        releaseName: "_js",
        action: "release",
        layerOptimize: "closure",
        optimize: "closure",
        cssOptimize: "comments",
        cssImportIgnore: "../dijit.css",
        mini: true,
        stripConsole: "warn",
        selectorEngine: "acme",

        defaultConfig: {
            hasCache:{
             "dojo-built": 1,
             "dojo-loader": 1,
             "dom": 1,
             "host-browser": 1,
             "config-selectorEngine": "acme"
            },
          async: 1
        },

        staticHasFeatures: {
//          "config-deferredInstrumentation": 1,
//          "config-dojo-loader-catches": 1,
//          "config-tlmSiblingOfDojo": 0,
//          "dojo-amd-factory-scan": 1,
//          "dojo-combo-api": 1,
//          "dojo-config-api": 1,
//          "dojo-config-require": 1,
//          "dojo-debug-messages": 1,
//          "dojo-dom-ready-api": 1,
            "dojo-firebug": 0,
            "dojo-guarantee-console": 0,
//          "dojo-has-api": 1,
//          "dojo-inject-api": 1,
//          "dojo-loader": 1,
//          "dojo-log-api": 1,
//          "dojo-modulePaths": 1,
//          "dojo-moduleUrl": 1,
//          "dojo-publish-privates": 1,
//          "dojo-requirejs-api": 1,
//          "dojo-sniff": 1,
//          "dojo-sync-loader": 1,
//          "dojo-test-sniff": 1,
//          "dojo-timeout-api": 1,
//          "dojo-trace-api": 1,
//          "dojo-undef-api": 1,
//          "dojo-v1x-i18n-Api": 1,
//          "dom": 1,
//          "host-browser": 1,
//          "extend-dojo": 1
        },

        packages:[{
            name: "dojo",
            location: "dojo"
        },{
            name: "dijit",
            location: "dijit"
        },{
            name: "dojox",
            location: "dojox"
        },{
            name: "gtcms",
            location: "gtcms"
        },{
	        name: "put-selector",
	        location: "put-selector"
	    },{
	        name: "dgrid",
	        location: "dgrid"
	    },{
	        name: "dstore",
	        location: "dstore"
	    },{
	        name: "rql",
	        location: "rql"
	    }],

        layers: {
            "dojo/dojo": {
                include: [
                    "dojo/dojo", "dojo/i18n", "dojo/domReady", "dojo/parser",
                    "gtcms/frontend"
                ],
                //                customBase: true,
                boot: true
            }
        }
    };
})();
