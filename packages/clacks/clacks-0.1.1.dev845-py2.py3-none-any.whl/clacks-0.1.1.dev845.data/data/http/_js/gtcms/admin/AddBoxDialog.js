define([
    'dojo/on',
    'dojo/_base/declare',
    'dijit/ConfirmDialog',
    'dijit/_WidgetBase',
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    '../dstores/boxes',
    'dojo/text!./templates/AddBoxDialog.html',
    //required by template:
    'dijit/form/Form',
    'dijit/form/ValidationTextBox',
    'dijit/form/Select'
], function (
    on, declare,
    Dialog, _Widget, _TemplatedMixin, _WidgetsInTemplateMixin,
    controlsStore, template
) {
    function show(ctrlList) {

        var content = new (declare([_Widget, _TemplatedMixin, _WidgetsInTemplateMixin], {
            templateString: template, //get template via dojo loader or so
            //message: message,
            destroy: function() {
                this.inherited(arguments);
            }
        }))();

        content.startup();

        var myDialog = Dialog({
            title: "Dodawanie artykułu",
            content: content
            //style: "width: 300px"
        });

        on(myDialog.okButton,
           'click',
           function(event) {
               if (content._form.validate()) {
                   controlsStore.add({
                       'label': content._label.get('value'),
                       'lang': content._lang.get('value'),
                       'title': content._title.get('value'),
                   }).then(function () {
                       if (ctrlList) {
                           ctrlList.refresh();
                       }
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
