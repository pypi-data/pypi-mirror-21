/*
 * UserProfilePane.js
 */

define([
    'dojo/_base/declare',
    'dojo/when',
    'dojo/on',
    'dojo/dom-style',
    'dojo/dom-geometry',
    "put-selector/put",
    'dijit/layout/ContentPane',
    'dijit/TitlePane',
    'dijit/layout/BorderContainer',
    'dijit/layout/TabContainer',
    'dijit/form/Button',
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    'dgrid/OnDemandGrid',
    'dgrid/extensions/DijitRegistry',
    'dgrid/extensions/ColumnReorder',
    'dgrid/extensions/ColumnResizer',
    'gtcms/dgrid/IndexColumn',
    'dgrid/Keyboard',
    'gtcms/session',
    'gtcms/admin/panel',
    'gtcms/dstores/users',
    'dojo/text!./templates/UserProfilePane.html',
    // preloads needed by template
    'dijit/form/TextBox',
    'dijit/form/Button',
    'dijit/form/CheckBox',
    'dijit/form/ValidationTextBox',
    'gtcms/admin/UserRelationSelect'
], function (
    declare, when, on, domStyle, domGeometry, put,
    ContentPane, TitlePane, BorderContainer, TabContainer, Button,
    _Templated, _WidgetsInTemplate,
    Grid, GridDijitRegistry, GridReorder, GridResizer, IndexColumn, GridKeyboard,
    session, panel, store,
    template
) {
    function _(a) { return a; }

    var mainPanes = {};
    function openPane(userid) {
        var user, operationsGrid;

        if (userid == 'new' || userid === undefined) {
            userid = 'new';
            user = when({'addresses': []});
        }
        else if (userid=='me') {
            user = store.get('me');
        }
        else {
            var useridn = parseInt(userid);
            if (useridn>0) {
                user = store.get(useridn);
            }
        }
        user.then(function (user) {
            var messagePane, boxPane, propsReady, activeAddressIdx=0;

            function setContents() {
                if (!propsReady)
                    return;

                if (user.id) {
                    boxPane._login.set('value', user.login);
                    boxPane._email.set('value', user.email);
                    boxPane._creationDate.innerHTML = user.created;
                    boxPane._phone.set('value', user.phone);
                    boxPane._fax.set('value', user.fax);
                    boxPane._profile.set('value', user.role);
                    boxPane._parent.set('value', user._parent);
                    boxPane._active.set('value', ''+user.active);

                    boxPane._name.set('value', user.name);
                    boxPane._surname.set('value', user.surname);
                    boxPane._company.set('value', user.company);
                    boxPane._vatid.set('value', user.vatid);

                    domStyle.set(boxPane._invitationMailPane, 'display', user.active ? 'none' : 'block');
                    domStyle.set(boxPane._restorePassword, 'display', user.active ? 'block' : 'none');
                }

                updateAddressForm();
            }

            function updateAddressForm() {
                if (user.addresses.length) {
                    activeAddressIdx = Math.max(activeAddressIdx, 0);
                    activeAddressIdx = Math.min(activeAddressIdx,user.addresses.length-1);
                    boxPane._recipient.set('value', user.addresses[activeAddressIdx].recipient);
                    boxPane._street.set('value', user.addresses[activeAddressIdx].street);
                    boxPane._postcode.set('value', user.addresses[activeAddressIdx].postcode);
                    boxPane._city.set('value', user.addresses[activeAddressIdx].city);
                    boxPane._country.set('value', user.addresses[activeAddressIdx].country);
                    boxPane._addresses_count.innerHTML = user.addresses.length;
                    boxPane._address_nr.innerHTML = activeAddressIdx+1;
                }
                else {
                    boxPane._recipient.set('value', '');
                    boxPane._street.set('value', '');
                    boxPane._postcode.set('value', '');
                    boxPane._city.set('value', '');
                    boxPane._country.set('value', '');
                }
                boxPane._recipient.set('disabled',
                                       (user.addresses.length === 0) || (activeAddressIdx === 0));
                boxPane._street.set('disabled', user.addresses.length === 0);
                boxPane._postcode.set('disabled', user.addresses.length === 0);
                boxPane._city.set('disabled', user.addresses.length === 0);
                boxPane._country.set('disabled', user.addresses.length === 0);
                boxPane._no_address_msg.style.display = (user.addresses.length) ? 'none' : 'inline';
                boxPane._address_nr_msg.style.display = (user.addresses.length) ? 'inline' : 'none';
            }

            function syncAddressForm() {
                if (user.addresses.length) {
                    user.addresses[activeAddressIdx].recipient = boxPane._recipient.value;
                    user.addresses[activeAddressIdx].street = boxPane._street.value;
                    user.addresses[activeAddressIdx].postcode = boxPane._postcode.value;
                    user.addresses[activeAddressIdx].city = boxPane._city.value;
                    user.addresses[activeAddressIdx].country = boxPane._country.value;
                }
            }

            function refreshAddress() {
                if (user.addresses.length) {
                    var company = boxPane._company.value.trim();
                    var recipient = (boxPane._name.value.trim()+' '+
                                     boxPane._surname.value.trim());
                    if (company.length) {
                        if (company.indexOf(recipient) !== -1) {
                            user.addresses[0].recipient = company;
                        }
                        else {
                            user.addresses[0].recipient = company+', '+recipient;
                        }
                    }
                    else {
                        user.addresses[0].recipient = recipient;
                    }
                    if (activeAddressIdx === 0) {
                        boxPane._recipient.set('value', user.addresses[0].recipient);
                    }
                }
            }

            if (!mainPanes[userid]) {

                mainPanes[userid] = new BorderContainer({
                    gutters: true,
                    title: ((user.name+user.surname) ? user.name+' '+user.surname :
                            (user.id ? user.login : _('Nowy użytkownik'))),
                    closable: true,
                    onClose: function () {
                        mainPanes[userid] = undefined;
                        return true;
                    }
                });


                boxPane = declare([ContentPane, _Templated, _WidgetsInTemplate], {
                    templateString: template,
                    title: _('Dane użytkownika'),
                    doLayout: false,
                    duration: 0,
                    region: 'top',
                    style: "border-width: 0px; padding: 0px;",

                    postCreate: function() {
                        this.inherited(arguments);
                    },

                    startup: function () {
                        this.inherited(arguments);
                        var self = this;
                        propsReady = true;

                        this._password1.validate = function(isFocused) {
                            if (this.value.length < 8  && this.value.length) {
                                this._set('state', 'Error');
                                this.set('message', _('podane hasło jest zbyt krótkie'));
                                return  false;
                            }
                            this._set('state', '');
                            this.set('message', '');
                            return true;
                        };

                        var auser = session.status();
                        if (auser.group == 'supervisor') {
                            domStyle.set(self._profileRowNode, 'display', 'none');
                        }

                        boxPane._parent.set('user', userid);

                        on(boxPane._prev_address_btn, 'click',
                          function () {
                              syncAddressForm();
                              activeAddressIdx--;
                              updateAddressForm();
                          });

                        on(boxPane._next_address_btn, 'click',
                          function () {
                              syncAddressForm();
                              activeAddressIdx++;
                              updateAddressForm();
                          });

                        on(boxPane._add_address_btn, 'click',
                          function () {
                              syncAddressForm();
                              user.addresses[user.addresses.length] = {
                                  "recipient": '',
                                  'label': '',
                                  'postcode': '',
                                  'province': '',
                                  'country': '',
                                  'lat': null,
                                  'lon': null,
                                  'city': '',
                                  'street': ''
                              };
                              activeAddressIdx = user.addresses.length-1;
                              updateAddressForm();
                              refreshAddress();
                          });

                        on(boxPane._del_address_btn, 'click',
                          function () {
                              user.addresses.splice(activeAddressIdx, 1);
                              activeAddressIdx--;
                              updateAddressForm();
                          });

                        on(boxPane._invitationMail, 'change', function (state) {
                            if (state) {
                                boxPane._active.set('value', 'true');
                            }
                        });

                        boxPane._name.set('intermediateChanges', true);
                        boxPane._surname.set('intermediateChanges', true);
                        boxPane._company.set('intermediateChanges', true);

                        on(boxPane._name, 'change', refreshAddress);
                        on(boxPane._surname, 'change', refreshAddress);
                        on(boxPane._company, 'change', refreshAddress);


                        this._password2.validate = function(isFocused) {
                            if (this.value.length && self._password1.value!=this.value) {
                                this._set('state', 'Error');
                                this.set('message', _('podane hasła nie są identyczne'));
                                return false;
                            }
                            if (!this.value.length && self._password1.value.length) {
                                this._set('state', 'Error');
                                this.set('message', _('należy ponownie wpisać hasło'));
                                return false;
                            }
                            this._set('state', '');
                            this.set('message', '');
                            return true;
                        };

                        setContents();

                        var _resize = function() {
                            var nHeight = domGeometry.getContentBox(self._propsPane.domNode).h+'px';
                            domStyle.set(boxPane.domNode, 'height', nHeight);
                            mainPanes[userid].resize();
                        };
                        on(this._propsPane, 'show', _resize);
                        on(this._propsPane, 'hide', _resize);
                    }
                })();

                var accPane = new TabContainer({
                    region: 'center'
                });

                /*
                require(['gtcms/dstores/ordersStore'], function(ordersStore) {

                var ordersGrid = new (declare(
                    [Grid, GridDijitRegistry,
                     GridReorder, GridResizer, GridKeyboard]))({
                         pagingDelay: 400,
                         columns: [
                            IndexColumn({field: 'idx', label: ""}),
                             { field: 'type', label: _('Operacja') },
                             { field: 'operationDate', label: _('Data') },
                             { field: 'income', label: _('Przychód') },
                             { field: 'debt', label: _('Rozchód') },
                             { field: 'recipient', label: _('Strona') },
                         ],
                         collection: ordersStore,
                         getBeforePut: false,
                     });
                });

                if (user.id) {
                    // needs to be replaced by modularization and events passing
                    if (operationsGrid) {
                        operationsGrid.set('query', {_user: user.id});
                    }
                    if (ordersGrid) {
                        ordersGrid.set('query', {_user: user.id});
                    }
                }

                var ordersPane = accPane.addChild(new ContentPane({
                    title: 'Zamówienia',
                    style: 'padding: 5px; margin: 0px;',
                    content: ordersGrid.domNode,
                }));
                */
                /*
                  require(['gtcms/dstores/walletOperationsStore'], function(operationsStore) {
                    operationsGrid = new (declare([Grid, GridDijitRegistry,
                                                       GridReorder, GridResizer, GridKeyboard]))(
                        {
                            pagingDelay: 400,
                            columns: [
                                IndexColumn({field: 'idx', label: ""}),
                                { field: 'type', label: _('Operacja') },
                                { field: 'operationDate', label: _('Data') },
                                { field: 'income', label: _('Przychód'),
                                  get: function(item) {
                                      return (item._fromUser != user.id) ? item.amount : '';
                                  }
                                },
                                { field: 'debt', label: _('Rozchód'),
                                  get: function(item) {
                                      return (item._fromUser == user.id) ? item.amount : '';
                                  }
                                },
                                { field: 'recipient', label: _('Strona'),
                                  get: function(item) {
                                      return ((item._fromUser != user.id)
                                              ? item.fromUserFullName : item.toUserFullName);
                                  }
                                },
                            ],
                            collection: operationsStore,
                            getBeforePut: false,
                        });

                    var operationsPane = accPane.addChild(new ContentPane({
                        title: 'Transakcje',
                        style: 'padding: 5px; margin: 0px;',
                        content: operationsGrid.domNode,
                    }));
                });*/

                var locationPane = new ContentPane({
                    title: 'Lokalizacja',
                    style: 'padding: 0px; margin: 0px; color: #ccc; overflow: hidden;'
                });

                accPane.addChild(locationPane);

                on(locationPane, 'Show',
                   function() {
                       put(locationPane.domNode, 'iframe',
                           { frameborder: "0",
                             width: '100%',
                             height: '100%',
                             scrolling: "no",
                             marginheight: "0",
                             marginwidth: "0",
                             src: "http://www.openstreetmap.org/export/embed.html?bbox=19.450864791870114%2C51.72548636662692%2C19.49150562286377%2C51.75397441189407&amp;layer=mapnik&amp;marker=51.73973263438796%2C19.471206665039062"});
                       return;
                       /*require(
                           ['/_js/OpenLayers/lib/OpenLayers.js',
                            'xstyle/css!/_js/OpenLayers/theme/default/style.css'],
                           function() {
                               var map = new OpenLayers.Map('userLocation');
                               var layer = new OpenLayers.Layer.OSM( "Simple OSM Map");
                               map.addLayer(layer);
                               / * map.setCenter(
                                  new OpenLayers.LonLat(-71.147, 42.472).transform(
                                  new OpenLayers.Projection("EPSG:4326"),
                                  map.getProjectionObject()
                                  ), 12
                                  );* /
                           });*/
                   });


                var submit = Button({
                    label: 'Zapisz zmiany',
                    region: 'right',
                    style: 'border-width: 0px; margin: 0px 0px 0px 5px;',
                    onClick: function () {
                        if (boxPane._form.validate()) {
                            refreshAddress();
                            syncAddressForm();
                            messagePane.set('content', _('Zapisywanie zmian'));
                            var newData = {
                                login: boxPane._login.value,
                                email: boxPane._email.value,
                                name: boxPane._name.value,
                                surname: boxPane._surname.value,
                                active: boxPane._active.get('value'),
                                phone: boxPane._phone.value,
                                vatid: boxPane._vatid.value,
                                fax: boxPane._fax.value,
                                company: boxPane._company.value,
                                //wantsVatInvoice,
                                role: boxPane._profile.value,
                                _parent: boxPane._parent.get('value')
                            };
                            if (newData.active && !user.active && boxPane._invitationMail.checked) {
                                newData.activationMail = true;
                            }

                            if (user.addresses !== undefined) {
                                newData.addresses = user.addresses;
                            }

                            if (boxPane._password1.value.length) {
                                newData.password = boxPane._password1.value;
                            }
                            if  (userid!='new') {
                                newData.id = userid;
                            }

                            store[newData.id ? 'put' : 'add'](newData).then(function(nitem) {
                                user = nitem;
                                if (userid == 'new') {
                                    mainPanes[user.id] = mainPanes['new'];
                                    mainPanes['new'] = undefined;
                                    userid = user.id;
                                }
                                setContents();
                                mainPanes[userid].set('title',
                                                        (user.name+user.surname) ?
                                                        user.name+' '+user.surname :
                                                        user.login);

                                messagePane.set('content', _('Zmiany zostały zapisane'));
                            });
                        }
                        else {
                            messagePane.set('content',
                                            _('Akcja wstrzymana. Błędnie wypełniony formularz.'));
                        }
                    }
                });

                /* needs to be conditional somehow */
                /*
                var addControl = Button({
                    label: 'Przekaż środki',
                    region: 'left',
                    style: 'border-width: 0px; margin: 0px 5px 0px 0px;'
                });
                */
                messagePane = ContentPane({
                    content: '',
                    region: 'center',
                    style: "margin: 0px 0px 0px 0px; padding: 4px 6px;"
                });
                var btnPane = BorderContainer({
                    region: 'bottom',
                    gutters: false,
                    style: "min-height: 26px; width: 100%; border-width: 0px; padding: 0px;"
                });
                btnPane.addChild(messagePane);
                btnPane.addChild(submit);
                //btnPane.addChild(addControl);

                mainPanes[userid].addChild(boxPane);
                mainPanes[userid].addChild(accPane);
                mainPanes[userid].addChild(btnPane);
                panel.tabs.addChild(mainPanes[userid]);
            }
            panel.tabs.selectChild(mainPanes[userid]);
        });
    }

    panel.addUrlHandler('user', function (uid) {
        openPane(parseInt(uid));
    });

    panel.addMenuItem({
        label: _('Profil'),
        section: _('Ustawienia'),
        priority: 90,
        onClick: function() {
            var user = session.status();
            if (user) {
                openPane('me');
            }
        }
    });

    return {'show': openPane};
});
