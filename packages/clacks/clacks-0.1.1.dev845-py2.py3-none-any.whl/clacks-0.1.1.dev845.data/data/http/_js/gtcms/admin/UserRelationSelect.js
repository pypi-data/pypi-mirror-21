define(['dojo/_base/declare',
        'dijit/_Widget',
        'dijit/form/FilteringSelect',
        'dojo/store/JsonRest'
],
function(
    declare, _Widget, FilteringSelect, JsonRest
) {
    return declare(
        [ FilteringSelect ],
        {
            user: undefined,

            constructor: function(args, domNode) {
                args.searchDelay = 100;
                args.autoComplete =  false;
                //args.hasDownArrow = false;
                args.searchAttr = "fullNameAndRole";
                args.labelAttr = "fullNameAndRole";
                args.required = false;
                args.store = new JsonRest({target: ('/_v1/users-names/'+
                                                    (args.user ? args.user+'/' : 'new/'))});
                args.queryExpr = '*${0}*';
                this.inherited(arguments);
            },
            _setUserAttr: function(user) {
                this._set('user', user);
                this.set('store', new JsonRest(
                    {target: ('/_v1/users-names/'+
                              (user ? user+'/' : 'new/'))}));
            }
        });
});
