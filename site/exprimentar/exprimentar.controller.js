(function () {
    'use strict';

    angular
        .module('app')
        .controller('ExprimentarController', ExprimentarController);

    ExprimentarController.$inject = ['$location', 'GraphsService', '$rootScope'];
    function ExprimentarController($location, GraphsService, $rootScope) {
        var vm = this;
        
        vm.getalltweets = getalltweets;
        vm.loadGraphGood = loadTableBad;
        vm.loadGraphGoodName = loadTableGood;
        vm.loadGraphBad = loadTableSpam;
        
    function getalltweets() {
            GraphsService.GetAllInfo(function(response){
                vm.dataLoading = true;
                if (response.success) {
                    vm.dataLoading = false;
                    loadTableGood($rootScope.datagood);
                    loadTableSpam($rootScope.dataspam);
                    loadTableBad($rootScope.databad);
                    loadTimeGraphGoodMinute($rootScope.datagood);
                    loadTimeGraphBadMinute($rootScope.databad);
                    loadTimeGraphGoodSec($rootScope.datagood);
                    loadTimeGraphBadSec($rootScope.databad);
                    
                }
                else{
                    alert(response);
                }
            });
        }
        
function loadTimeGraphBadMinute(data)
        {
            var timeChart = dc.lineChart("#dc-time-chart-badMin");
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
function loadTimeGraphGoodMinute(data)
        {
            var timeChart = dc.lineChart("#dc-time-chart-goodMin");
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
        
        function loadTimeGraphBadSec(data)
        {
            var timeChart = dc.lineChart("#dc-time-chart-badSec");
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
function loadTimeGraphGoodSec(data)
        {
            var timeChart = dc.lineChart("#dc-time-chart-goodSec");
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

        function loadTableGood(data){
            $(document).ready(function() {
                        var t = $('#tabela1').DataTable({"autoWidth": false});
                        var counter = 1;
                            for (var key in data)
                            {
                            var aux = t.row.add( [
                                data[String(key)]['id'],
                                data[String(key)]['id_str'],
                                data[String(key)]['n_followers'],
                                data[String(key)]['location'],
                                data[String(key)]['name'],
                                data[String(key)]['friends_count'],
                                data[String(key)]['time'],
                                data[String(key)]['tweet'],
                                data[String(key)]['guess']
                            ] ).draw( false );
                            }
                            
                            counter++;
                        });
  }
        function loadTableBad(data){
            $(document).ready(function() {
                        var t = $('#tabela2').DataTable({"autoWidth": false});
                        var counter = 1;
                            for (var key in data)
                            {
                            var aux = t.row.add( [
                                data[String(key)]['id'],
                                data[String(key)]['id_str'],
                                data[String(key)]['n_followers'],
                                data[String(key)]['location'],
                                data[String(key)]['name'],
                                data[String(key)]['friends_count'],
                                data[String(key)]['time'],
                                data[String(key)]['tweet'],
                                data[String(key)]['guess']
                            ] ).draw( false );
                            }
                            
                            counter++;
                        });
  }
        function loadTableSpam(data){
            $(document).ready(function() {
                        var t = $('#tabela3').DataTable({"autoWidth": false});
                        var counter = 1;
                            for (var key in data)
                            {
                            var aux = t.row.add( [
                                data[String(key)]['id'],
                                data[String(key)]['id_str'],
                                data[String(key)]['n_followers'],
                                data[String(key)]['location'],
                                data[String(key)]['name'],
                                data[String(key)]['friends_count'],
                                data[String(key)]['time'],
                                data[String(key)]['tweet'],
                                data[String(key)]['guess']
                            ] ).draw( false );
                            }
                            
                            counter++;
                        });
  }
        }

})();