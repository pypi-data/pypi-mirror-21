/*
 * LoginsGraphs.js
 */

define([
    "dojo",
    "dojo/_base/declare",
    "dojo/currency",
    "dojo/fx/easing",
    "dijit/layout/BorderContainer",
    "dijit/layout/ContentPane",
    'dijit/_TemplatedMixin',
    'dijit/_WidgetsInTemplateMixin',
    "dijit/form/DateTextBox",
    "dojox/charting/Chart",
    "dojox/charting/StoreSeries",
    "dojox/charting/themes/Claro",
    "dojox/charting/plot2d/Lines",
    "dojox/charting/plot2d/Spider",
    "dojox/charting/action2d/Tooltip",
    "dojox/charting/action2d/Magnify",
    "dojox/charting/plot2d/Markers",
    "dojox/charting/axis2d/Default",
    "put-selector/put",
    "gtcms/admin/panel",
    "gtcms/stores/loginsStatsStore",
    "gtcms/stores/loginsDayCycleStore",
    "gtcms/stores/loginsWeekCycleStore",
    "gtcms/stores/registrationsStatsStore",
    "dojo/text!../templates/LoginsGraphsPane.html",
    "xstyle/css!/_js/dgrid/css/skins/claro.css"
], function (
    dojo, declare, currency,
    easing, BorderContainer,
    ContentPane, _Templated, _WidgetsInTemplate, DateTextBox,
    Chart, StoreSeries, chartTheme, LinesPlot, SpiderPlot, ChartTooltip,
    ChartMagnify, ChartMarkers, ChartDefault,
    put,
    panel, loginsStore, dayCycleStore, weekCycleStore, registrationsStore, template
) {
    var mainPane;

    var openPane = function () {
        var dailyChart, regChart, daysChart, hoursChart, dateFromField, dateToField;
        wdays = ['Niedziela', 'Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela'];

        function labelfTime(o, a, e) {
            var dt = new Date();
            if (a) {
                dt.setTime(a*1000);
            }
            else  {
                dt.setTime(o*1000);
            }
            var d = dt.getUTCDate()+'/'+(dt.getUTCMonth()+1)+"/"+dt.getUTCFullYear();
            return d;
        }


        if (!mainPane) {
            mainPane = new BorderContainer({
                gutters: true,
                title: "Stats: Logowania",
                closable: true,
                onClose: function () {
                    mainPane = undefined;
                    return true;
                }
            });

            var drawDayCycleChart = function (filter) {

                dayCycleStore.query(filter).then(function(data) {
                    var series = {};
                    var maxval = 1;
                    for(var key in data) {
                        series[""+key] = data[key].logins;
                        if (data[key].logins > maxval) {
                            maxval = data[key].logins;
                        }
                    }
                    mainStatsPane._hourly_logins.innerHTML = "";
                    hoursChart = new Chart(mainStatsPane._hourly_logins,
                                           {title: "Rozkład godzinowy logowań",
                                            titlePos: "top",
                                            titleFont: "normal normal normal 12px Arial",
                                            titleGap: 5,
                                            titleFontColor: '#aaa'
                                           });

                    var tmpseries = {};
                    for(var hour=0; hour<24; hour++) {
                        hoursChart.addAxis(""+hour, {max: maxval});
                        tmpseries[""+hour] = 0.001;
                    }

                    hoursChart.setTheme(chartTheme);

                    hoursChart.addPlot("default", {
                        type: SpiderPlot,
                        labelOffset: -10,
                        divisions: 2,
                        seriesFillAlpha: 0.7,
                        markerSize: 3,
                        precision: 0,
                        spiderType: "polygon",
                        spiderOrigin: 0.001,
                        markers: true,
                        animate: { duration: 300, easing: easing.linear}
                    });

                    hoursChart.addSeries("hours", {data: series}, { fill: "blue" });
                    hoursChart.addSeries("tmphours", {data: tmpseries}, { fill: "blue" });
                    hoursChart.render();
                });
            };

            var drawWeekCycleChart = function (filter) {
                weekCycleStore.query(filter).then(function(data) {
                    var series = {};
                    var maxval = 1;
                    for(var key in data) {
                        series[wdays[key]] = data[key].logins;
                        if (data[key].logins > maxval) {
                            maxval = data[key].logins;
                        }

                    }
                    mainStatsPane._weekly_logins.innerHTML = "";
                    daysChart = new Chart(mainStatsPane._weekly_logins,
                                          {title: "Rozkład tygodniowy logowań",
                                           titlePos: "top",
                                           titleFont: "normal normal normal 12px Arial",
                                           titleGap: 5,
                                           titleFontColor: '#aaa'
                                          });

                    var tmpseries = {};
                    for (var kday in wdays) {
                        daysChart.addAxis(wdays[kday], {max: maxval});
                        tmpseries[wdays[kday]] = 0.001;
                    }

                    daysChart.setTheme(chartTheme);
                    daysChart.addPlot("default", {
                        type: SpiderPlot,
                        labelOffset: -10,
                        divisions: 2,
                        seriesFillAlpha: 0.7,
                        markerSize: 3,
                        precision: 0,
                        spiderType: "polygon",
                        spiderOrigin: 0.002,
                        markers: true,
                        animate: { duration: 300, easing: easing.linear}
                    });

                    daysChart.addSeries("days", {data: series}, { fill: "blue" });
                    daysChart.addSeries("tmpdays", {data: tmpseries}, { fill: "blue" });
                    daysChart.render();
                });
                //var tip = new ChartTooltip(daysChart, "default");
                //var mag = new ChartMagnify(daysChart, "default");
            };

            var applyFilters = function () {
                if (!dateFromField.value.toJSON() || !dateToField.value.toJSON()) {
                    return;
                }
                var fromDate = dateFromField.value.toJSON().substring(0,10);
                var toDate = dateToField.value.toJSON().substring(0,10);
                dailyChart.updateSeries(
                    "Logowania",
                    new StoreSeries(loginsStore, {query: {from: fromDate, to:  toDate}},
                        function (item, store) {
                            dt = new Date();
                            dt.setTime(item.id*1000);
                            var o = {
                                x: item.id,
                                y: item.logins,
                                tooltip: labelfTime(item.id)+"<br />"+wdays[dt.getDay()]+
                                         "<br /> logowań: "+item.logins
                            };
                            return o;
                        }
                    ));
                dailyChart.resize().render();

                regChart.updateSeries(
                    "Registrations",
                    new StoreSeries(
                        registrationsStore, {query: {from: fromDate, to: toDate}},
                        function (item, store) {
                            dt = new Date();
                            dt.setTime(item.id*1000);
                            var o = {
                                x: item.id,
                                y: item.registrations,
                                tooltip: labelfTime(item.id)+"<br />"+wdays[dt.getDay()]+
                                        "<br /> rejestracji: "+item.registrations
                            };
                            return o;
                        }
                    ));
                regChart.resize().render();

                drawDayCycleChart({from: fromDate, to: toDate});
                drawWeekCycleChart({from: fromDate, to: toDate});

            };

            dateFromField = new DateTextBox({
                onChange: applyFilters});

            dateToField = new DateTextBox({
                onChange: applyFilters});

            var optionsPane = new ContentPane({
                style: "height: auto; border-width: 0px; padding: 0px; margin: 5px 0px 0px;",
                region: "top",
                content: "",
                postCreate: function () {
                    put(this.domNode, "div[style=$]", "float: left; padding: 0px 6px",
                        "Okres od: ", dateFromField.domNode);
                    put(this.domNode, "div[style=$]", "float: left; padding: 0px 6px",
                        "do: ", dateToField.domNode);
                }
            });

            var footerPane = new BorderContainer({
                style: "height: 1px; margin: 0px 5px; border-width: 0px; text-align: right; padding: 0px;",
                region: "bottom",
                gutters: false
            });


            var mainStatsPane = declare([ContentPane, _Templated, _WidgetsInTemplate], {
                templateString: template,
                "class": "loginStatsMainPane",
                style: "border: 0px; padding: 0px 0px;",
                region: "center",
                doLayout: true,
                startup: function () {
                    this.inherited(arguments);
                    setTimeout( function() {
                        dailyChart = new Chart(mainStatsPane._daily_logins,
                                               {title: "Logowania",
                                                titlePos: "top",
                                                titleFont: "normal normal normal 12px Arial",
                                                titleGap: 5,
                                                titleFontColor: '#aaa'
                                               });

                        // Set the theme
                        dailyChart.setTheme(chartTheme);

                        // Add the only/default plot
                        dailyChart.addPlot("default", {
                            type: LinesPlot,
                            markers: true,
                            animate: { duration: 300, easing: easing.linear}
                        });


                        // Add axes
                        dailyChart.addAxis("x", {labelFunc:labelfTime});
                        dailyChart.addAxis("y", {min: 1, vertical: true, fixUpper: "major", includeZero: true});
                        //dailyChart.setAxisWindow("x",8640,1)
                        dailyChart.addSeries(
                            "Logowania",
                            new StoreSeries(
                                loginsStore,
                                {},
                                function (item, store) {
                                    dt = new Date();
                                    dt.setTime(item.id*1000);
                                    var o = {
                                        x: item.id,
                                        y: item.logins,
                                        tooltip: labelfTime(item.id)+"<br />"+wdays[dt.getDay()]+
                                                "<br /> logowań: "+item.logins
                                    };
                                    return o;
                                }
                            ));
                        var tip = new ChartTooltip(dailyChart, "default");
                        var mag = new ChartMagnify(dailyChart, "default");

                        regChart = new Chart(mainStatsPane._daily_registrations,
                                               {title: "Rejestracje",
                                                titlePos: "top",
                                                titleFont: "normal normal normal 12px Arial",
                                                titleGap: 5,
                                                titleFontColor: '#aaa'
                                               });

                        // Set the theme
                        regChart.setTheme(chartTheme);

                        // Add the only/default plot
                        regChart.addPlot("default", {
                            type: LinesPlot,
                            markers: true,
                            animate: { duration: 300, easing: easing.linear}
                        });


                        // Add axes
                        regChart.addAxis("x", {labelFunc:labelfTime});
                        regChart.addAxis("y", {min: 1, vertical: true, fixUpper: "major", includeZero: true});

                        regChart.addSeries(
                            "Registrations",
                            new StoreSeries(
                                registrationsStore,
                                {},
                                function (item, store) {
                                    dt = new Date();
                                    dt.setTime(item.id*1000);
                                    var o = {
                                        x: item.id,
                                        y: item.registrations,
                                        tooltip: labelfTime(item.id)+"<br />"+wdays[dt.getDay()]+
                                                "<br /> rejestracji: "+item.registrations
                                    };
                                    return o;
                                }
                            ));
                        tip = new ChartTooltip(regChart, "default");
                        mag = new ChartMagnify(regChart, "default");

                        drawDayCycleChart({});
                        drawWeekCycleChart({});

                        setTimeout(function() {
                            dailyChart.resize().render();
                            regChart.resize().render();
                        }, 2000);
                    }, 400);
                },
                resize: function () {
                    this.inherited(arguments);
                    if (dailyChart && regChart && daysChart && hoursChart) {
                        dailyChart.resize().render();
                        regChart.resize().render();
                        hoursChart.resize().render();
                        daysChart.resize().render();
                    }
                }
            })();

            mainPane.addChild(optionsPane);
            mainPane.addChild(footerPane);
            mainPane.addChild(mainStatsPane);

            panel.tabs.addChild(mainPane);
        }
        panel.tabs.selectChild(mainPane);
    };

    panel.addMenuItem({
        label: "Logowania",
        section: "Statystyki",
        priority: 90,
        onClick: openPane
    });

    panel.addUrlHandler("login-graphs", openPane);

    return {"show": openPane};
});
