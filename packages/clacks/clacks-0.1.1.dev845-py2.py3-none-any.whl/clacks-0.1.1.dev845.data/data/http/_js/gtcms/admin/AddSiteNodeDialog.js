define([
    'require',
    'dojo/on',
    'dojo/_base/declare',
    'dijit/ConfirmDialog',
    'dijit/_WidgetBase',
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    '../dstores/siteNodes',
    '../stores/siteNodeTemplatesStore',
    'dojo/text!../templates/AddSiteNodeDialog.html',
    './SiteTree',
    //required by template:
    'dijit/form/Form',
    'dijit/form/TextBox',
    'dijit/form/Select',
    'dijit/form/RadioButton'
], function (
    require, on, declare,
    Dialog, _Widget, _TemplatedMixin, _WidgetsInTemplateMixin,
    nodesStore, templatesStore, template,
    SiteTree
) {
    function show(parentid) {

        var content = new (declare([_Widget, _TemplatedMixin, _WidgetsInTemplateMixin], {
            templateString: template, //get template via dojo loader or so
            //message: message,
            destroy: function() {
                this.inherited(arguments);
            }
        }))();

        content._type.set('labelAttr', 'name');
        content._type.set('query', {parent_page: parentid});
        content._type.set('store', templatesStore);
        content.startup();

        var myDialog = Dialog({
            title: "Dodawanie pozycji struktury",
            content: content
            //style: "width: 300px"
        });

        on(myDialog.okButton,
           'click',
           function(event) {
               var options = {};
               if (content._form.validate()) {
                   console.log(content._firstPosition.get('value'));
                   if (!content._firstPosition.get('value')) {
                       options.beforeId = null;
                   }
                   nodesStore.add({
                           '_parent': parentid,
                           'linkName': content._name.value,
                           'template': content._type.value
                       }, options
                   ).then(function(node) {
                       var pane = node.type[0].toUpperCase()+node.type.slice(1)+'Pane';
                       require(['./'+pane],
                               function(nodePane) {
                                   nodePane(node.id);
                               });
                       SiteTree.refresh();
                   });
                   setTimeout(function () {myDialog.destroyRecursive();}, 1000);
                   return true;
               }
               else {
                   event.stopPropagation();
                   return false;
               }
           });
        on(myDialog,
           'Cancel',
           function(/*event*/) {
               setTimeout(function () {myDialog.destroyRecursive();}, 1000);
           });
        myDialog.show();
    }

    return {show: show};
});
