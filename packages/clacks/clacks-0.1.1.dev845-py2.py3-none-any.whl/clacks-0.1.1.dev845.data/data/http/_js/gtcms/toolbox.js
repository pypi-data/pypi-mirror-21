
define([
    'dojo/dom-construct',
    'dojo/_base/window',
    'dojo/on',
    'dojo/domReady!'
],
function(
    domConstruct, win, on
) {
    var active = false;
    var isLoadStarted = false;

    if (window._ === undefined) {
        window._ = function(text) { return text; };
    }
    var btnToolBox = domConstruct.create(
        'div',
        { id: "toolbox-button",
          style: "position: fixed; top: 0px; left: 0px; padding: 4px; z-index: 1000;",
          innerHTML: "" },
        win.body());

    on(btnToolBox, "click", function() {
        require([
            'gtcms/toolboxDialog'
        ], function(
            toolBoxDialog
        ) {
            toolBoxDialog.toggle();
        });
    });
});
