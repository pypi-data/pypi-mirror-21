"use strict";

try {
    angular.module('googlechart');
    var app = angular.module('hidash', ['googlechart']);
    }
catch(e){
    var app = angular.module('hidash', []);
}


app.directive('hiDashGc', ['$http', 'resolveTemplate', 'urlProcessor',
    function($http, resolveTemplate, urlProcessor) {
        return {
            restrict: 'E',
            scope: {
                host: '@host',
                chart_name: '@chart',
                params: '=params',
                chart_type: '@type',
                update: '@update',
                options: '=options',
                typeSelect: '=typeSelect',
                container: '@container',
                noApiCall: '@noApiCall',
                chartData: '=?chartData'
            },
            controller: function($scope, $element) {
                if (!$scope.noApiCall) {
                    $scope.chartUrl = urlProcessor.generateUrl($scope.chart_name,
                    $scope.host);

                    if ($scope.params) {
                        $scope.chartUrl = urlProcessor.addParams($scope.params, $scope.chartUrl);
                    }
                } else {
                    $scope.chart.data = $scope.chartData;
                }
                var updateChartData = function() {
                    if (!$scope.noApiCall) {
                        $http.get($scope.chartUrl).success(function(data) {
                            $scope.chart.data = data;
                        });
                    } else {
                        $scope.chart.data = $scope.chartData;
                    }
                };
                var createChartSuccess = function (data) {
                    if ($scope.chart_type == 'MapChart') {
                        createMap(data);
                        return;
                    }
                    $scope.chart = {};
                    $scope.chart.data = data;
                    if ($scope.chart_type) {
                        $scope.chart.type = $scope.chart_type;
                    } else if (data.chart_type) {
                        $scope.chart.type = data.chart_type;
                    } else {
                        $scope.chart.type = "ColumnChart";
                    }
                    $scope.chart.options = $scope.options || {};
                    $scope.chartTypes = ["LineChart", "BarChart",
                        "ColumnChart", "AreaChart",
                        "PieChart", "ScatterChart",
                        "SteppedAreaChart", "ComboChart"
                    ];
                };
                var createChart = function() {
                    if (!$scope.noApiCall) {
                        $http.get($scope.chartUrl).success(function(data) {
                            createChartSuccess(data);
                        }).error(function(data) {
                            if ($scope.container) {
                                if (document.getElementById($scope.container)) {
                                    document.getElementById($scope.container).remove();
                                }
                            }
                        });
                    } else {
                        createChartSuccess($scope.chartData);
                    }
                };
                var createMap = function(data) {
                    google.load("visualization", "1", {
                        "packages": ["map"],
                        "callback": drawMap
                    });

                    function drawMap() {
                        var options = $scope.options || {};
                        options.showTip = true;
                        var map = new google.visualization.Map($element[0].firstChild);
                        map.draw(new google.visualization.DataTable(data), options);
                    }
                };
                if ($scope.update) {
                    setInterval(updateChartData, $scope.update);
                }
                $scope.$watch('[params,chart_name,host,options,chart_type,typeSelect,chartData,noApiCall]',
                    function(newValue, oldValue)  {
                        if (!newValue[6]) {
                            $scope.chartUrl = urlProcessor.generateUrl(newValue[1],
                                          newValue[2], newValue[3]);
                            if (newValue[0]) {
                               $scope.chartUrl = urlProcessor.addParams(newValue[0],
                               $scope.chartUrl);
                            }
                        } else {
                            $scope.chartData = newValue[5];
                        }
                        createChart();
                }, true);
            },
            template: resolveTemplate
        };
    }])
    .directive('hiDashHc', ['$http', 'urlProcessor',  function($http, urlProcessor) {
        return {
            restrict: 'E',
            scope: {
                host: '@host',
                chart_name: '@chart',
                params: '@params',
                chart_type: '@type',
                update: '@update',
                container: '@container',
                options: '=options',
                noApiCall: '@noApiCall',
                chartData: '=?chartData'
            },
            controller: function($scope, $element) {
                if (!$scope.noApiCall) {
                    $scope.chartUrl = urlProcessor.generateUrl($scope.chart_name, $scope.host);
                     if ($scope.params) {
                         $scope.chartUrl = urlProcessor.addParams($scope.params, $scope.chartUrl);
                     }
                 }
                function createChartSuccess(data) {
                    var chartData = {};
                    chartData.chart = {
                        type: 'column'
                    };
                    chartData.xAxis = {
                        type: 'category'
                    };
                    if($scope.options !== undefined) {
                        chartData = $scope.options;
                    }
                    chartData.series = data;
                    chartData.credits = {
                        enabled: false
                    };
                    if ($scope.chart_type) {
                        chartData.chart.type = $scope.chart_type;
                    }
                    var newChart = new Highcharts.chart($element[0],chartData);
                };
                function updateChartSuccess(data) {
                    var current_data_length = newChart.series.length;
                    var new_data_length = data.length;
                    var data_length = new_data_length;

                    if (current_data_length < new_data_length) {
                        data_length = current_data_length
                    }

                    for (var i = 0; i < new_data_length; i++) {
                        newChart.series[i].update({
                            name: data[i].name
                        });
                        newChart.series[i].setData(data[i].data);
                    }
                    while (i < current_data_length) {
                        newChart.series[i].remove();
                        i++;
                    }
                };
                var updateChart = function() {
                    if (!$scope.noApiCall) {
                        $http.get($scope.chartUrl).success(function(data) {
                            updateChartSuccess(data)
                        })
                    } else {
                        updateChartSuccess($scope.chartData)
                    }
                };
                var createChart = function() {
                    if (!$scope.noApiCall) {
                        $http.get($scope.chartUrl).success(function(data) {
                            createChartSuccess(data);
                            if ($scope.update) {
                                setInterval(updateChart, $scope.update);
                            }
                        }).error(function(data) {
                            if ($scope.container) {
                                if (document.getElementById($scope.container)) {
                                    document.getElementById($scope.container).remove();
                                }
                            }
                        });
                    } else {
                        createChartSuccess($scope.chartData);
                        if ($scope.update) {
                            setInterval(updateChart, $scope.update);
                        }
                    }
                };
                $scope.$watch('[params,chart_name,host,options,chart_type,chartData,noApiCall]',
                    function(newValue, oldValue) {
                        if (!newValue[6]) {
                            $scope.chartUrl = urlProcessor.generateUrl(newValue[1], newValue[2], newValue[3]);
                            if (newValue[0]) {
                               $scope.chartUrl = urlProcessor.addParams(newValue[0], $scope.chartUrl);
                            }
                        } else {
                            $scope.chartData = newValue[5];
                        }
                        createChart();
                }, true);
            }
        };
    }])
    .directive('hiDashTableWidgets', ["urlProcessor", "$http", function(urlProcessor, $http) {
        return {
            restrict: 'E',
            scope: {
                host: '@host',
                widget_name: '@widget',
                params: '@params',
                update: '@update',
                container: '@container',
                options: '=options',
                widgetData: '=?widgetData',
                noApiCall: '@noApiCall',
                noHeader: '@noHeader',
                widgetHeight: '@widgetHeight'
            },
            controller: function($scope, $element) {
                $scope.widgetId = $scope.widget_name.replace(/ /g,"_");
                $scope.widgetAPIData = [];

                if (!$scope.noApiCall) {
                    $scope.widgetUrl = urlProcessor.generateUrl($scope.widget_name, $scope.host);
                    if ($scope.params) {
                        $scope.chartUrl = urlProcessor.addParams($scope.params, $scope.widgetUrl);
                    }
                }
                var updateWidget = function() {
                    if (!$scope.noApiCall) {
                        $http.get($scope.widgetUrl).success(function(data) {
                            $scope.widgetAPIData = angular.copy(data.widget_data);
                        })
                    } else {
                        $scope.widgetAPIData = $scope.widgetData;
                    }
                };
                var createWidget = function() {
                    if (!$scope.noApiCall) {
                        $http.get($scope.chartUrl).success(function(data) {
                            $scope.widgetAPIData = angular.copy(data.widget_data);
                            if ($scope.update) {
                                setInterval(updateWidget, $scope.update);
                            }
                        }).error(function(data) {
                            if ($scope.container) {
                                if (document.getElementById($scope.container)) {
                                    document.getElementById($scope.container).remove();
                                }
                            }
                        });
                    } else {
                        $scope.widgetAPIData = $scope.widgetData;
                        if ($scope.update) {
                            setInterval(updateWidget, $scope.update);
                        }
                    }
                };
                $scope.$watch('[params,widget_name,host,options,noApiCall,widgetData]', function(newValue, oldValue) {
                    if (newValue[4]) {
                        $scope.widgetUrl = urlProcessor.generateUrl(newValue[1], newValue[2], newValue[3]);
                        if (newValue[0]) {
                           $scope.widgetUrl = urlProcessor.addParams(newValue[0], $scope.widgetUrl);
                        }
                    } else {
                        $scope.widgetData = newValue[5];
                    }
                    createWidget();
                }, true);
            },
            template: '<div id={{widgetId}} class="hi-dash-widget">'+
                '<h3 ng-if="!noHeader">{{widget_name}}</h3>'+
                '<div ng-style="{height: widgetHeight+px}"><table class="table">'+
                '<tbody><tr ng-repeat="rowData in widgetAPIData"'+
                'ng-style="{height: widgetHeight/widgetAPIData.length +px}">'+
                '<td ng-repeat="cols in rowData">{{cols}}</td>'+
                '</tr></tbody></table></div></div>'
        }
    }])
    .directive('hcChart', function () {
        return {
            restrict: 'A',
            scope: {
                options: '=',
                chartId: '@'
            },
            controller: function ($scope, $element) {
                $scope.$watch('options', function (newVal, oldVal) {
                    $("#"+$scope.chartId).highcharts(newVal);
                }, true);
            }
        };
    })
    .directive('hiDashReports', ['$http','urlProcessor', function($http, urlProcessor) {
        return {
            restrict: 'E',
            scope: {
                host: '@host',
                group: '@group',
                params: '@params',
                renderFlag: '=renderFlag'
            },
            controller: function($scope, $element) {
                $scope.startDate = new Date();
                $scope.startDate.setDate(1);
                $scope.endDate = new Date();
                $scope.endDate.setMonth($scope.endDate.getMonth() + 1);
                $scope.endDate.setDate(1);
                $scope.chartUrl = urlProcessor.generateReportUrl($scope.host, $scope.group);
                $scope.createWidgetId = function (str) {
                    var tempId = str.replace(/ /g, "_") + "_report";
                    return tempId.toLowerCase();
                };

                $scope.createHighchartId = function (str) {
                    var tempId = str.replace(/ /g, "_") + "_highcharts";
                    return tempId.toLowerCase();
                };

                if($scope.params !== undefined) {
                    $scope.chartUrl = urlProcessor.addParams($scope.params, $scope.chartUrl);
                }
                var createReport = function() {
                    $http.get($scope.chartUrl).success(function(data) {
                        $scope.data = data;
                        $scope.chartData = new Array($scope.data.length);
                        for(var i=0; i < $scope.data.length; i++) {
                            $scope.data[i].grid_width = $scope.data[i].grid_width || 12;
                            if($scope.data[i].handler_type === "highcharts") {
                                var chartType = $scope.data[i].chart_type || 'column',
                                    loadHichart = $scope.data[i].chart_data[0].data.length;

                                $scope.chartData[i] = {
                                    title: '',
                                    chart: {
                                        type: chartType
                                    },
                                    xAxis: {
                                        type: 'category',
                                        minPadding: 0,
                                        maxPadding: 0
                                    },
                                    series: $scope.data[i].chart_data,
                                    credits: {
                                        enabled: false
                                    },
                                    load: loadHichart
                                };
                            } else if($scope.data[i].handler_type === "googlechart" || $scope.data[i].handler_type === "hidash") {
                                $scope.chartData[i]={};
                                $scope.chartData[i].data = $scope.data[i].chart_data;
                                $scope.chartData[i].type = $scope.data[i].chart_data.chart_type;

                                if ($scope.data[i].chart_data.type === "widget") {
                                    $scope.chartData[i].load = $scope.data[i].chart_data.widget_data.length;
                                } else if ($scope.data[i].chart_data.chart_type === "Table") {
                                    $scope.chartData[i].load = $scope.data[i].chart_data.rows.length;
                                }
                            }
                        }
                    });
                };
                $scope.$watch('params', function (newVal, oldVal) {
                    if($scope.renderFlag === true) {
                        $scope.chartUrl = urlProcessor.addParams(newVal, urlProcessor.generateReportUrl($scope.host, $scope.group));
                        createReport();
                    }
                }, true);
            },
            template:
                    '<section class="row" class="report-area" id="hidash_reports_section">'+
                    '<div ng-repeat="chart in data track by $index" class=\'hi-dash-print {{"col-md-"+chart.grid_width}}\''+
                    ' id={{createWidgetId(chart.chart_id)}} ng-if="chartData[$index].load">'+
                    '<h3>{{chart.chart_id}} <div ng-if="chart.description" class="hidash-description">{{chart.description}}</div>'+
                    '</h3><hi-dash-table-widgets ng-if="chart.handler_type===\'hidash\' && chart.chart_type===\'widget\'" widget="{{chart.chart_id}}" no-api-call="true" no-header="true" widget-data="chart.chart_data.widget_data"'+
                    'widget-height="{{chart.height}}"></hi-dash-table-widgets>'+
                    '<div ng-if="chart.handler_type===\'highcharts\'" id={{createHighchartId(chart.chart_id)}} chart-id="{{createHighchartId(chart.chart_id)}}"'+
                    'options="chartData[$index]" hc-chart></div>'+
                    '<div ng-if="chart.handler_type===\'googlechart\'" google-chart class="hi-google-print" chart="chartData[$index]"style="height: {{chart.height}}px"></div>'+
                    '</div></section>'
        };
    }])
    .directive('hiDashNamedDateFilters', function() {
        return {
            restrict: 'E',
            scope: {
                options: '=',
                filterId: '@',
                labelName: '@',
                selected: '=',
                getDateFromName: '&getDateFromName',
                gridwidth: '@'
            },
            template: '<div class=\'{{"col-md-"+gridwidth}}\'>'+
            '<h3 ng-if="labelName">{{labelName}}</h3>'+
            '<button class="btn btn-default hidash-named-filter btn-space" ng-repeat="data in options" ng-if="data.active" type="button" value={{data.range}}'+
            'id=\'{{"hidash_dtperiod_"+$index}}\' ng-click="getDateFromName({selectedValue: data.range})">{{data.range}}</button>'+
            '</div>'
        };
    })
    .service('resolveTemplate', function() {
        return function(tElement, tAttrs) {
            if(tAttrs.type == "MapChart") {
                return '<div style="height:100%; width: 100%;"></div>';
            }
            if(tAttrs.typeselect == 'am') {
                return '<md-input-container class="chart-select"><md-select ng-model="chart.type"><md-option ng-repeat="type in chartTypes" value="{{type}}">{{type}}</md-option></md-select></md-input-container><div google-chart chart="chart" style="height:100%; width: 100%;"></div>';
            }
            else if(tAttrs.typeselect == 'bs') {
                return '<div class="col-xs-3"><select ng-model="chart.type" class="wrapper form-control chart-select"><option ng-repeat="type in chartTypes" value={{type}}>{{type}}</option></select></div><div google-chart chart="chart"></div>';
            }
            else if(tAttrs.typeselect == 'true') {
                return '<div ><select ng-model="chart.type" class="chart-select"><option ng-repeat="type in chartTypes" value={{type}}>{{type}}</option></select></div><div google-chart chart="chart"></div>';
            }
            else {
                return '<div google-chart chart="chart"></div>';
            }
        };
    })
    .service('urlProcessor', function() {
        var _addParams = function(params, url) {
            var processed_params = params.replace(/\s*(,|^|$)\s*/g, "$1").split(',');
            for (var index = 0; index < processed_params.length; index++) {
                if (url.indexOf('?') == -1) {
                    url += "?" + processed_params[index];
                }
                else{
                url += "&" + processed_params[index];}
            }
            return url;
        };
        var _generateUrl = function(name, host) {
            var url = "/hidash-api/charts/" + name + ".json/";
            if (typeof CONFIG !== 'undefined') {
                url = CONFIG.hidashApiBase + "/charts/" + name + ".json/";
            } else if (host !== undefined) {
                url = host + "/hidash-api/charts/" + name + ".json/";
            }
            return url;
        };
        var _generateReportUrl = function(host, group) {
            var url = "/hidash-api/show_reports.json/";
            if (typeof CONFIG !== 'undefined') {
                url = CONFIG.hidashApiBase + "/show_reports.json/";
            } else if (host !== undefined) {
                url = host + "/show_reports.json/";
            }
            if (group !== undefined) {
                url = url + "?group=" + group;
            }
            return url;
        };

        return {
            addParams: _addParams,
            generateUrl: _generateUrl,
            generateReportUrl: _generateReportUrl
        };
    });

