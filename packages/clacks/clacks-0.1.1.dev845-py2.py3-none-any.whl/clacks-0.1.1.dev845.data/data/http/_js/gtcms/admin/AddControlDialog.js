define([
    'dojo/on',
    'dojo/_base/declare',
    'dijit/ConfirmDialog',
    'dijit/_WidgetBase',
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    '../dstores/controls',
    '../stores/controlFactoryStore',
    'dojo/text!./templates/AddControlDialog.html',
    //required by template:
    'dijit/form/Form',
    'dijit/form/TextBox',
    'dijit/form/Select',
    'dijit/form/RadioButton'
], function (
    on, declare,
    Dialog, _Widget, _TemplatedMixin, _WidgetsInTemplateMixin,
    controlsStore, factoryStore, template
) {
    function show(pageid, ctrlList) {

        var content = new (declare([_Widget, _TemplatedMixin, _WidgetsInTemplateMixin], {
            templateString: template, //get template via dojo loader or so
            //message: message,
            destroy: function() {
                this.inherited(arguments);
            }
        }))();

        content._type.set('labelAttr', 'fullname');
        content._type.set('query', {nodeid: pageid});
        content._type.set('store', factoryStore);
        content.startup();

        var myDialog = Dialog({
            title: "Dodawanie elementu strony",
            content: content
            //style: "width: 300px"
        });

        on(myDialog.okButton,
           'click',
           function(event) {
               if (content._form.validate()) {
                   controlsStore.add({
                       '_page': pageid,
                       'type': content._type.value.split(':')[0],
                       'placement': content._type.value.split(':')[1]
                   }).then(function () {
                       ctrlList.refresh();
                   });
                   setTimeout(function () {myDialog.destroyRecursive();}, 1000);
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
