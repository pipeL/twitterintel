(function () {
    'use strict';

    angular
        .module('app')
        .controller('TopwordsgraphsController3', TopwordsgraphsController3);

    TopwordsgraphsController3.$inject = ['$location', 'GraphsService', '$rootScope'];
    function TopwordsgraphsController3($location, GraphsService , $rootScope) {
        var vm = this;

        vm.loadGraphGood= loadGraphGood;
        vm.loadGraphBad= loadGraphBad;
        vm.loadGraphSpam= loadGraphSpam;
        vm.loadPieGraph= loadPieGraph;
        
        vm.refresh = refresh;
        
        
        function refresh(data){
            GraphsService.GetAllGraphs3(function(response){
                vm.dataLoading = true;
                if (response.success) {
                    vm.dataLoading = false;
                    loadPieGraph($rootScope.Total);
                    loadGraphGood($rootScope.GoodData);
                    loadGraphBad($rootScope.BadData);
                    loadGraphSpam($rootScope.SpamData);
                    
                }
                else{
                    alert(response);
                }
            })
            vm.dataLoading=false;
        }
        function loadPieGraph(data){
  var chart = dc.pieChart("#contagemtotal");

  var ndx           = crossfilter(data),
      runDimension  = ndx.dimension(function(d) {return d.tipo;}),
      speedSumGroup = runDimension.group().reduceSum(function(d) {return d.contagem;});

  chart
  .width(1000)
  .height(600)
  .slicesCap(4)
  .innerRadius(100)
  .dimension(runDimension)
  .group(speedSumGroup)
  .legend(dc.legend())
  .on('pretransition', function(chart) {
  chart.selectAll('text.pie-slice').text(function(d) {
  return d.data.key + ' ' + dc.utils.printSingleValue((d.endAngle - d.startAngle) / (2*Math.PI) * 100) + '%';
        })
    });

  chart.render();
  }
 function loadGraphGood(data)
  {
  var chart = dc.barChart("#good");
  var ndx = crossfilter(data);
  var folDimension = ndx.dimension(function(d) { return d.word;});
  var folGroup = folDimension.group().reduceSum(function(d) { return +d.count;});

  chart
        .width(1000)
        .height(600)
        .x(d3.scale.ordinal().domain(data.map(function(d) { return d.word;})))
        .brushOn(false)
        .yAxisLabel("This is the Good Chart!")
        .dimension(folDimension)
        .group(folGroup)
        .xUnits(dc.units.ordinal)
        .on('renderlet', function(chart) {
            chart.selectAll('rect').on("click", function(d) {
                console.log("click!", d.x);
            });
        });
  chart.render();
  }
    
    
    
function loadGraphBad(data)
  {
  var chart = dc.barChart("#bad");
  var ndx = crossfilter(data);
  var folDimension = ndx.dimension(function(d) { return d.word;});
  var folGroup = folDimension.group().reduceSum(function(d) { return +d.count;});

  chart
        .width(1000)
        .height(600)
        .x(d3.scale.ordinal().domain(data.map(function(d) { return d.word;})))
        .brushOn(false)
        .yAxisLabel("This is the BAD Chart!")
        .dimension(folDimension)
        .group(folGroup)
        .xUnits(dc.units.ordinal)
        .on('renderlet', function(chart) {
            chart.selectAll('rect').on("click", function(d) {
                console.log("click!", d.x);
            });
        });
  chart.render();
  }
    
function loadGraphSpam(data)
  {
  var chart = dc.barChart("#spam");
  var ndx = crossfilter(data);
  var folDimension = ndx.dimension(function(d) { return d.word;});
  var folGroup = folDimension.group().reduceSum(function(d) { return +d.count;});

  chart
        .width(1000)
        .height(600)
        .x(d3.scale.ordinal().domain(data.map(function(d) { return d.word;})))
        .brushOn(false)
        .yAxisLabel("This is the SPAM Chart!")
        .dimension(folDimension)
        .group(folGroup)
        .xUnits(dc.units.ordinal)
        .on('renderlet', function(chart) {
            chart.selectAll('rect').on("click", function(d) {
                console.log("click!", d.x);
            });
        });
  chart.render();
  }
    }

})();