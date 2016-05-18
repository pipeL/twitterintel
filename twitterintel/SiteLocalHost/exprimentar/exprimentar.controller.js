(function () {
    'use strict';

    angular
        .module('app')
        .controller('ExprimentarController', ExprimentarController);

    ExprimentarController.$inject = ['$location', 'GraphsService', '$rootScope'];
    function ExprimentarController($location, GraphsService, $rootScope) {
        var vm = this;
        
        vm.getalltweets = getalltweets;
        vm.loadGraphGood = loadGraphGood;
        vm.loadGraphGoodName = loadGraphGoodName;
        vm.loadGraphBad = loadGraphBad;
        
    function getalltweets() {
            GraphsService.GetAllInfo(function(response){
                vm.dataLoading = true;
                if (response.success) {
                    vm.dataLoading = false;
                    loadGraphGood($rootScope.datagood);
                    loadGraphGoodName($rootScope.datagood);
                    loadGraphBad($rootScope.databad);
                    loadTimeGraphGood($rootScope.datagood);
                    loadTimeGraphBad($rootScope.databad);
                    
                }
                else{
                    alert(response);
                }
            });
        }
        
function loadTimeGraphGood(data)
        {
            var timeChart = dc.lineChart("#dc-time-chart-good");
            var dtgFormat = d3.time.format("%Y-%m-%dT%H:%M:%S");
              var dtgFormat2 = d3.time.format("%a %e %b %H:%M");

              data.forEach(function(d) {
                d.dtg = dtgFormat.parse(d.time.substr(0,19)); 

              });
            var facts = crossfilter(data);
            var volumeByHour = facts.dimension(function(d) {
                return d3.time.minute(d.dtg);
              });
            var volumeByHourGroup = volumeByHour.group()
                .reduceCount(function(d) { return d.dtg; });
            
            timeChart.width(960)
            .height(150)
            .transitionDuration(500)
        //    .mouseZoomable(true)
            .margins({top: 10, right: 10, bottom: 20, left: 40})
            .dimension(volumeByHour)
            .group(volumeByHourGroup)
        //    .brushOn(false)			// added for title
            .title(function(d){
              return dtgFormat2(d.data.key)
              + "\nNumber of Events: " + d.data.value;
              })
            .elasticY(true)
            .x(d3.time.scale().domain(d3.extent(data, function(d) { return d.dtg; })))
            .xAxis();
            
         timeChart.render();   
            
            
            
        }
function loadTimeGraphBad(data)
        {
            var timeChart = dc.lineChart("#dc-time-chart-bad");
            var dtgFormat = d3.time.format("%Y-%m-%dT%H:%M:%S");
              var dtgFormat2 = d3.time.format("%a %e %b %H:%M");

              data.forEach(function(d) {
                d.dtg = dtgFormat.parse(d.time.substr(0,19)); 

              });
            var facts = crossfilter(data);
            var volumeByHour = facts.dimension(function(d) {
                return d3.time.second(d.dtg);
              });
            var volumeByHourGroup = volumeByHour.group()
                .reduceCount(function(d) { return d.dtg; });
            
            timeChart.width(960)
            .height(150)
            .transitionDuration(500)
        //    .mouseZoomable(true)
            .margins({top: 10, right: 10, bottom: 20, left: 40})
            .dimension(volumeByHour)
            .group(volumeByHourGroup)
        //    .brushOn(false)			// added for title
            .title(function(d){
              return dtgFormat2(d.data.key)
              + "\nNumber of Events: " + d.data.value;
              })
            .elasticY(true)
            .x(d3.time.scale().domain(d3.extent(data, function(d) { return d.dtg; })))
            .xAxis();
            
         timeChart.render();   
            
            
            
        }

function loadGraphGood(data)
  {
  var chart = dc.barChart("#good");
  var ndx = crossfilter(data);
  var folDimension = ndx.dimension(function(d) { return d.location;});
  var folGroup = folDimension.group().reduce(

            function (p, d) {
                if (d.location in p.locations) p.locations[d.location]++;
                else {
                    p.locations[d.location] = 1;
                    p.locationCount++;
                }
                return p;
            },

            function (p, d) {
                p.locations[d.location]--;
                if (p.locations[d.location] === 0) {
                    delete p.locations[d.location];
                    p.locationCount--;
                }
                return p;
            },

            function () {
                return {
                    locationCount: 0,
                    locations: {}
                };
            });

  chart
        .width(500)
        .height(300)
        .x(d3.scale.ordinal().domain(data.map(function(d) { return d.location;})))
        .brushOn(false)
        .yAxisLabel("This is the Bad Chart!")
        .dimension(folDimension)
        .group(folGroup)
        .valueAccessor(function (d) {
            return d.value.locationCount;
        })
        .xUnits(dc.units.ordinal)
        .on('renderlet', function(chart) {
            chart.selectAll('rect').on("click", function(d) {
                console.log("click!", d.x);});
            chart.selectAll("g.x text").attr('dx', '-30').attr(
  'dy', '-7').attr('transform', "rotate(90)");
            
        });
  chart.render();
  }
    
    function loadGraphGoodName(data)
  {
  var chart = dc.barChart("#namegood");
  var ndx = crossfilter(data);
  var folDimension = ndx.dimension(function(d) { return d.name;});
  var folGroup = folDimension.group().reduce(

            function (p, d) {
                if (d.name in p.names) p.names[d.name]++;
                else {
                    p.names[d.name] = 1;
                    p.nameCount++;
                }
                return p;
            },

            function (p, d) {
                p.names[d.name]--;
                if (p.names[d.name] === 0) {
                    delete p.names[d.name]; 
                    p.nameCount--;
                }
                return p;
            },

            function () {
                return {
                    nameCount: 0,
                    names: {}
                };
            });

  chart
        .width(500)
        .height(300)
        .x(d3.scale.ordinal().domain(data.map(function(d) { return d.name;})))
        .brushOn(false)
        .yAxisLabel("This is the Bad Chart!")
        .dimension(folDimension)
        .group(folGroup)
        .valueAccessor(function (d) {
            return d.value.nameCount;
        })
        .xUnits(dc.units.ordinal)
        .on('renderlet', function(chart) {
            chart.selectAll('rect').on("click", function(d) {
                console.log("click!", d.x);});
            chart.selectAll("g.x text").attr('dx', '-30').attr(
  'dy', '-7').attr('transform', "rotate(90)");
            
        });
  chart.render();
  }
    
    function loadGraphBad(data)
  {
  var chart = dc.barChart("#bad");
  var ndx = crossfilter(data);
  var folDimension = ndx.dimension(function(d) { return d.location;});
  var folGroup = folDimension.group().reduce(

            function (p, d) {
                if (d.location in p.locations) p.locations[d.location]++;
                else {
                    p.locations[d.location] = 1;
                    p.locationCount++;
                }
                return p;
            },

            function (p, d) {
                p.locations[d.location]--;
                if (p.locations[d.location] === 0) {
                    delete p.locations[d.location];
                    p.locationCount--;
                }
                return p;
            },

            function () {
                return {
                    locationCount: 0,
                    locations: {}
                };
            });

  chart
        .width(500)
        .height(300)
        .x(d3.scale.ordinal().domain(data.map(function(d) { return d.location;})))
        .brushOn(false)
        .yAxisLabel("This is the Good Chart!")
        .dimension(folDimension)
        .group(folGroup)
        .valueAccessor(function (d) {
            return d.value.locationCount;
        })
        .xUnits(dc.units.ordinal)
        .on('renderlet', function(chart) {
            chart.selectAll('rect').on("click", function(d) {
                console.log("click!", d.x);});
            chart.selectAll("g.x text").attr('dx', '-30').attr(
  'dy', '-7').attr('transform', "rotate(90)");
            
        });
  chart.render();
  }
    }

})();