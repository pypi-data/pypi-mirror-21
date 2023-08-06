/**
 *
 */
define([
    'dojo/_base/declare',
    'dojo/when',
    'dojo/_base/xhr',
    'dojo/_base/config',
    'dojo/DeferredList',
    'dojo/_base/lang',
    'dojo/dom-construct',
    'dojo/query',
    'dojo/on',
    "put-selector/put",
    'gtcms/session',
    'dijit/layout/AccordionContainer',
    'dijit/layout/AccordionPane',
    'dijit/layout/LayoutContainer',
    'dijit/layout/BorderContainer',
    'dijit/layout/TabContainer',
    'dijit/layout/ContentPane',
    'dijit/MenuBar',
    'dijit/PopupMenuBarItem',
    'dijit/MenuBarItem',
    'dijit/MenuItem',
    'dijit/DropDownMenu',
    '../locale',
    'dijit/TitlePane',
    'xstyle/css!/_css/gtlogo.css'
], function(
    declare, when, xhr, config, DeferredList, lang, domConstruct, query, on, put, session,
    AccordionContainer, AccordionPane,
    LayoutContainer, BorderContainer, TabContainer, ContentPane,
    MenuBar, PopupMenuBarItem, MenuBarItem, MenuItem, DropDownMenu, _
) {

    function _(text) {return text;}

    var _Panel = declare(null, {

        _waitFor: [],
        /**
         * collects list of deferreds to wait for before initially showing
         * interface after call to this.run()
         */
        waitFor: function(defer) {
            if (defer) {
                this._waitFor.push(defer);
            }
        },

        _menuItems: [],

        addMenuItem: function(elem) {
            if (!elem.section) {
                elem.section = 'Treści';
            }
            this._menuItems.push(elem);
        },

        _urlHandlers: {},
        addUrlHandler: function(name, callback) {
            this._urlHandlers[name] = callback;
        },

        constructor: function () {
            var that = this;
            this.bodyContainer = new LayoutContainer({
                style: 'width: 100%; height: 100%;',
                design: 'headline'
            });

            var topMenu = this.topMenu = new ContentPane({
                region: 'top',
                'class': 'topMenuPane'
            });

            this.bodyContainer.addChild(this.topMenu);



            this.mainContainer = new BorderContainer({region: 'center'});

            var leftPane = new AccordionContainer({
                region: 'left',
                maxSize: '100px'

            });
            this._menuPane = new ContentPane({
                'content': put('div.leftMenu'),
                region: 'left',
                'class': 'leftMenuPane'
            });

            this.bodyContainer.addChild(this._menuPane);

            that.tabs = new TabContainer({region: 'center', tabStrip: true});
            this.mainContainer.addChild(that.tabs);

            this.bodyContainer.addChild(this.mainContainer);

            this.waitFor(
                when(session.status(), function(sess) {
                    topMenu.domNode.innerHTML = (
                        '<div class="topMenuVersionInfo">'+
                        '<span>'+config.ver+'</span>'+
                        '<span>gtCMS</span>'+
                        '<span style="margin-left: 6px; margin-right: -3px;"'+
                        ' class="small gtsymbol"></span></div>');

                    put(topMenu.domNode, 'span', _('Użytkownik: '));
                    put(topMenu.domNode, 'span', sess.username);

                    dojo.forEach(sess.menuItems, function(menuItem) {
                        that.addMenuItem({
                            label: menuItem.label,
                            section: menuItem.section,
                            onClick: lang.hitch(that, 'onOldMenuClick', menuItem),
                            priority: menuItem.priority});
                    });
                })
            );

           that.addMenuItem({
               label: 'Wyloguj',
               onClick: lang.hitch(that,'logout'),
               section: 'Ustawienia',
               priority: 2000
           });
           window.setInterval(function () {
               session.status();
           }, 30000);
        },

        _oldMenuTabs: [],
        onOldMenuClick: function(item) {
            var that = this;
            if (!this._oldMenuTabs[item.label]) {
                this._oldMenuTabs[item.label] = new ContentPane({
                    title: item.label,
                    closable: true,
                    style: "padding: 0px; overflow: hidden;",
                    content: '<iframe style="width: 100%; height: 100%; border-width: 0px;"></iframe>',
                    onClose: function () {
                        that._oldMenuTabs[item.label] = undefined;
                        return true;
                    }
                });
                this.tabs.addChild(this._oldMenuTabs[item.label]);
            }
            this._oldMenuTabs[item.label].set('title', item.label);
            query('iframe', this._oldMenuTabs[item.label].containerNode).attr('src', '/'+item.url);
            this.tabs.selectChild(this._oldMenuTabs[item.label]);
        },

        run: function() {
            var that = this;
            new DeferredList(this._waitFor).then(function() {

                that._menuItems.sort(function (a, b) {
                    return ((1-(a.section == b.section)-(a.section < b.section)*2) ||
                            (a.priority-b.priority) ||
                            (1-(a.label == b.label)-(a.label < b.label)*2));
                });
                var targetNode = query('.leftMenu', that._menuPane.containerNode)[0];
                var blockName = '';
                dojo.forEach(that._menuItems, function(item) {
                    if (blockName !== (item.section || 'Treści')) {
                        put(targetNode, 'div.leftMenuSection',
                            { innerHTML: item.section || 'Treści'});
                        blockName = item.section || 'Treści';
                    }
                    on(put(targetNode, 'a.leftMenuItem', item.label),
                       'click',
                       item.onClick);
                });

                domConstruct.place(that.bodyContainer.domNode, query('body')[0], 'first');
                that.bodyContainer.startup();
            });
            if (location.hash) {
                var elems = location.hash.split('#');
                for (var idx=1; idx < elems.length; idx++) {
                    var elem = elems[idx];
                    var params = elem.split(',');
                    if (that._urlHandlers[params[0]]) {
                        that._urlHandlers[params[0]](params.slice(1));
                    }
                }
            }
        },

        logout: function() {
            query('body').forEach(domConstruct.empty);
            session.logout().then(function() {location.reload(true);});
        }
    });

    var panel = new _Panel();
    // temporarily here (hopefully)
    panel.addUrlHandler('page', function (args) {
        if (args[0]=='id') {
                panel.onOldMenuClick({"label": "Strona: ("+args[1]+")",
                                      "url":'admin_article.php?id='+args[1]});
        }
    });

    return panel;
});
