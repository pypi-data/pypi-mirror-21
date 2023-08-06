define([
    'dojo/_base/declare',
    'dojo/dom-geometry',
    'dijit/TitlePane'
], function (
    declare, domGeom, TitlePane
) {
    return declare([TitlePane], {
        toggleable: false,
        doLayout: true,

        resize: function(dims) {
            var containerSize = domGeom.getContentBox(this.containerNode);
            var artSize = domGeom.getContentBox(this.domNode);
            var artTBarSize = domGeom.getMarginBox(this.domNode.children[0]);
            //console.log([containerSize.h, artSize.h, artTBarSize.h]);
            this.containerNode.style.height = dims.h-artTBarSize.h-22+'px';
            this.inherited(arguments);
        }
    });
});
