var hidashApp = angular.module('dashboard', ['googlechart','hidash', 'ui.bootstrap']);
hidashApp.config(function($locationProvider) {
    $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    });
});
hidashApp.controller('ReportsController',function($scope, $http, $window, $location, utils){
  $scope.filters = [];
  $scope.renderFlag = false;
  $scope.group = '';
  if('group' in $location.search()) {
    $scope.group = $location.search()['group'];
    $http.get('/hidash-api/get_group_filters.json/?group=' + $scope.group).success(function(filters) {
      $scope.filters = filters;
      $scope.paramsList = [];
      $scope.parameters = [];
      $scope.filterLabels = [];
      for (var i = 0; i < $scope.filters.length; i++) {
        if($scope.filters[i].type === 'datetime') {
          $scope.filterLabels.push($scope.filters[i].name.replace(/_/g, " "));
          var date = new Date();
          date.setDate(1);
          if($scope.filters[i].filter_value !== null){
            date = $scope.filters[i].filter_value;
          }
          date = $location.search()[$scope.filters[i].name] ? $location.search()[$scope.filters[i].name] : date;
          $scope.parameters.push(date);
          }
        else if($scope.filters[i].type === 'daterange') {
          var labels = [$scope.filters[i].name[0].replace(/_/g, " "), $scope.filters[i].name[1].replace(/_/g, " ")];
          $scope.filterLabels.push(labels);
          var start_date = new Date();
          var end_date = new Date();
          start_date.setDate(1);
          end_date.setDate(3);
          if($scope.filters[i].filter_value !== null){
            start_date = $scope.filters[i].filter_value[0];
            end_date = $scope.filters[i].filter_value[1];
          }
          start_date = $location.search()[$scope.filters[i].name[0]] ? $location.search()[$scope.filters[i].name[0]]: start_date;
          end_date = $location.search()[$scope.filters[i].name[1]] ? $location.search()[$scope.filters[i].name[1]]: end_date;
          date = [start_date, end_date];
          $scope.parameters.push(date);
        } else if ($scope.filters[i].type === 'periodicDatePicker') {
          var labels = "Date Filters", tempOptions = $scope.filters[i].filter_value, selectedDate;
          var periodicValue;
          if($location.search().periodicDatePicker) {
            periodicValue = $location.search().periodicDatePicker
          }
          else {
            periodicValue = 'Reset'
          }
          selectedDate = $scope.filters[i].selectedValue = periodicValue
          $scope.filters[i].filterType = $location.search()["periodicDatePicker"] || selectedDate;
          var results = utils.getDateFromNameDate(selectedDate),
          tempDefault = {};
          tempDefault[$scope.filters[i].name[0]] = results.startDate;
          tempDefault[$scope.filters[i].name[1]] = results.endDate;
          tempDefault["periodicDatePicker"] = $scope.filters[i].filterType;
          $scope.parameters.push(tempDefault);

          $scope.filterLabels.push(labels);
        }
        else {
          $scope.filterLabels.push($scope.filters[i].name.replace(/_/g, " "));
          var dropdownParam = '1';
          dropdownParam = $location.search()[$scope.filters[i].name] ? $location.search()[$scope.filters[i].name] : dropdownParam;
          var dropdownArr = $scope.filters[i].filter_values, paramObj = {};
          for (var l = 0; l < dropdownArr.length; l++) {
            if (dropdownArr[l].value === dropdownParam) {
              paramObj.name = dropdownArr[l].name;
              paramObj.value = dropdownArr[l].value;
            }
          }
          $scope.parameters.push(paramObj);
        }
      }
      $scope.$watch('parameters', function() {
        newParams = '';
        urlParamsObj = {group: $scope.group};
        for (var  i= 0;i<$scope.parameters.length;i++) {
          if($scope.filters[i].type === 'datetime') {
            newParams += $scope.filters[i].name + '=' + moment($scope.parameters[i]).format("YYYY-MM-DD") + ',';
            urlParamsObj[$scope.filters[i].name] = moment($scope.parameters[i]).format("YYYY-MM-DD");
          } else if ($scope.filters[i].type === 'daterange') {
            newParams += $scope.filters[i].name[0] +'=' + moment($scope.parameters[i][0]).format("YYYY-MM-DD 00:00:00") +','+$scope.filters[i].name[1] +'=' + moment($scope.parameters[i][1]).format("YYYY-MM-DD 23:59:59") + ',';
            urlParamsObj[$scope.filters[i].name[0]] = moment($scope.parameters[i][0]).format("YYYY-MM-DD 00:00:00");
            urlParamsObj[$scope.filters[i].name[1]] = moment($scope.parameters[i][1]).format("YYYY-MM-DD 23:59:59");
          } else if ($scope.filters[i].type === 'periodicDatePicker') {
            newParams += $scope.filters[i].name[0]+'='+$scope.parameters[i][$scope.filters[i].name[0]]+','+$scope.filters[i].name[1]+'='+$scope.parameters[i][$scope.filters[i].name[1]];
            urlParamsObj["periodicDatePicker"] = $scope.filters[i].filterType ;
          } else {
            newParams += $scope.filters[i].name + '=' + $scope.parameters[i].value + ',';
            urlParamsObj[$scope.filters[i].name] = $scope.parameters[i].value;
          }
        }
        $scope.params = newParams;
        $location.search(urlParamsObj);
      }, true);
      $scope.renderFlag = true;
    });
  }
  $scope.getDateFromName = function (data, index) {
    var results = {}, tempDefault = {};
    if (typeof data !== "object") {
      results = utils.getDateFromNameDate(data);
      $scope.filters[index].filterType = data;
    } else {
      results = data;
      $scope.filters[index].filterType = "custom";
    }
    tempDefault[$scope.filters[index].name[0]] = results.startDate;
    tempDefault[$scope.filters[index].name[1]] = results.endDate;
    tempDefault["periodicDatePicker"] = data;
    $scope.parameters[index] = tempDefault;
  }
})
.directive('hiDash', ['$http', function($http) {
  return {
    restrict: 'E',
    template:
    "<div id='dashboard' class='container'>"+
      "<div class='hidash-dashboard-filter row'>"+
        "<div ng-repeat='filter in filters'>"+
          "<div class='date'>"+
            '<div ng-if="filter.type===\'datetime\'">'+
              '<div class="col-md-{{filter.grid_width}} col-xs-{{filter.grid_width}}">'+
              "<label class='filter-labels'>{{filterLabels[$index]}}</label>"+
              "<p class='input-group'>"+
                "<input type='text' class='form-control' datepicker-popup='dd MMM yyyy' date-time-picker-set-local ng-model='parameters[$index]' datepicker-options='dateOptions' name='HidashStartDate' show-weeks='false' close-text='Close' ng-model-onblur/>"+
                "<span class='input-group-btn input-group-hidash-icon'>"+
                  "<i class='fa fa-calendar' aria-hidden='true'></i>"+
                "</span>"+
                "</p>"+
                "</div>"+
              "</div>"+
              '<div ng-if="filter.type===\'dropdown\'">'+
                '<div class="col-md-{{filter.grid_width}} col-xs-{{filter.grid_width}}">'+
                "<label class='filter-labels'>{{filterLabels[$index]}}</label>"+
                '<select ng-model="parameters[$index]" class="form-control" ng-options="value.name for value in filter.filter_values track by value.value">'+
                '</select>'+
                '</div>'+
              "</div>"+
              '<div ng-if="filter.type===\'daterange\'">'+
              '<div class="col-md-{{filter.grid_width}} col-xs-{{filter.grid_width}}">'+
              "<label class='filter-labels'>{{filterLabels[$index][0]}}</label>"+
              "<p class='input-group'>"+
                "<input type='text' class='form-control' datepicker-popup='dd MMM yyyy' date-time-picker-set-local ng-model='parameters[$index][0]' datepicker-options='dateOptions' name='HidashStartDateRange' show-weeks='false' close-text='Close' ng-model-onblur/>"+
                "<span class='input-group-btn input-group-hidash-icon'>"+
                  "<i class='fa fa-calendar' aria-hidden='true'></i>"+
                "</span>"+
                "</p>"+
              '</div>'+
              '<div class="col-md-{{filter.grid_width}} col-xs-{{filter.grid_width}}">'+
                "<label class='filter-labels'>{{filterLabels[$index][1]}}</label>"+
                "<p class='input-group'>"+
                "<input type='text' class='form-control' datepicker-popup='dd MMM yyyy' date-time-picker-set-local ng-model='parameters[$index][1]' datepicker-options='dateOptions' name='HidashEndDateRange' show-weeks='false' close-text='Close' ng-model-onblur/>"+
                "<span class='input-group-btn input-group-hidash-icon'>"+
                  "<i class='fa fa-calendar' aria-hidden='true'></i>"+
                "</span>"+
                "</p>"+
              "</div>"+
              "</div>"+
              '<div ng-if="filter.type===\'periodicDatePicker\'">'+
              '<hi-dash-named-date-filters options="filter.filter_value" filterId="{{filter.type}}" get-date-from-name="getDateFromName(selectedValue, $index)" selected="filter.selectedValue" gridwidth="{{filter.grid_width}}" ng-model="parameters[$index].periodicDatePicker" filter-type="filter.filterType"/>'+
              '</div>'+
          "</div>"+
        "</div>"+
      "</div>"+
      "<hi-dash-reports group={{group}} params='{{params}}' render-flag='renderFlag'></hi-dash-reports>"+
    "</div>"
  };
}])
.directive('pageOverlayPace', function($window) {
    return {
        restrict: 'E',
        template: '<div class="pace-overlay"></div>',
        link: function (scope, element) {
            //Fixme: Pace issue, start event is not firing on page load.
            //Using this workaround to handle it.
            element.ready(function() {
                $("div.pace-overlay").show();
            });
            Pace.on("start", function(){
                $("div.pace-overlay").show();
            });

            Pace.on("done", function(){
                $("div.pace-overlay").hide();
            });
        }
    }
})
.service('utils', function() {
    var getDateFromNameDate = function(dateName) {
            let dateOptions = ['Today', 'Yesterday', 'Tomorrow', 'This Week', 'This Month', 'This Year', 'Last Week', 'Last Month', 'Last Year', 'Reset']
        let dateOptionsObj = {}

        dateOptions.map((name) => {
            dateOptionsObj[name] = {}
        })

        dateOptionsObj = {
            "Today": {
                startDate: moment().format("YYYY-MM-DD 00:00:00"),
                endDate: moment().format("YYYY-MM-DD 23:59:59")
            },
            "Yesterday": {
                startDate: moment().subtract(1, 'days').format("YYYY-MM-DD 00:00:00"),
                endDate: moment().subtract(1, 'days').format("YYYY-MM-DD 23:59:59")
            },
            "Tomorrow": {
                startDate: moment().add(1, 'days').format("YYYY-MM-DD 00:00:00"),
                endDate: moment().add(1, 'days').format("YYYY-MM-DD 23:59:59")
            },
            "This Week": {
                startDate: moment().startOf('isoweek').format("YYYY-MM-DD 00:00:00"),
                endDate: moment().format("YYYY-MM-DD 23:59:59")
            },
            "This Month": {
                startDate: moment().startOf('month').format("YYYY-MM-DD 00:00:00"),
                endDate: moment().format("YYYY-MM-DD 23:59:59")
            },
            "This Year": {
                startDate: moment().startOf('year').format("YYYY-MM-DD 00:00:00"),
                endDate: moment().format("YYYY-MM-DD 23:59:59")
            },
            "Current Week": {
                startDate: moment().startOf('isoweek').format("YYYY-MM-DD 00:00:00"),
                endDate: moment().endOf('isoweek').format("YYYY-MM-DD 23:59:59")
            },
            "Current Month": {
                startDate: moment().startOf('month').format("YYYY-MM-DD 00:00:00"),
                endDate: moment().endOf('month').format("YYYY-MM-DD 23:59:59")
            },
            "Current Year": {
                startDate: moment().startOf('year').format("YYYY-MM-DD 00:00:00"),
                endDate: moment().endOf('year').format("YYYY-MM-DD 23:59:59"),
            },
            "Next Week": {
                startDate: moment().endOf('isoweek').add(1, 'days').format("YYYY-MM-DD 00:00:00"),
                endDate: moment().endOf('isoweek').add(7, 'days').format("YYYY-MM-DD 23:59:59")
            },
            "Last Week": {
                startDate: moment().startOf('isoweek').subtract(7, 'days').format("YYYY-MM-DD 00:00:00"),
                endDate: moment().endOf('isoweek').subtract(7, 'days').format("YYYY-MM-DD 23:59:59")
            },
            "Last Month": {
                startDate: moment().subtract(1, 'months').startOf('month').format("YYYY-MM-DD 00:00:00"),
                endDate: moment().subtract(1, 'months').endOf('month').format("YYYY-MM-DD 23:59:59")
            },
            "Last Year": {
                startDate: moment().subtract(1, 'year').startOf('year').format("YYYY-MM-DD 00:00:00"),
                endDate: moment().subtract(1, 'year').endOf('year').format("YYYY-MM-DD 23:59:59")
            },
            'Reset': {
              startDate: '2010-11-01',
              endDate: '2100-12-20'
            }
        }
        return dateOptionsObj[dateName]
    }
    return {
      getDateFromNameDate: getDateFromNameDate
    }
})



