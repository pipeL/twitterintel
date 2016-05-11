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
            var table = $('#tabela').DataTable();
            var table1 = $('#tabela1').DataTable();
            var table2 = $('#tabela2').DataTable();
 
            table
                .destroy();
            table1
                .destroy();
            table2
                .destroy();
            GraphsService.GetAllGraphs3(function(response){
                vm.dataLoading = true;
                if (response.success) {
                    vm.dataLoading = false;
                    loadPieGraph($rootScope.Total);
                    loadGraphGood($rootScope.GoodData);
                    loadGraphBad($rootScope.BadData);
                    loadGraphSpam($rootScope.SpamData);
                    $('#third').show();
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
  var chart = dc.barChart("#graph1");
  var ndx = crossfilter(data);
  var folDimension = ndx.dimension(function(d) { return d.word;});
  var folGroup = folDimension.group().reduceSum(function(d) { return +d.count;});

  chart
        .width(667)
        .height(580)
        .x(d3.scale.ordinal().domain(data.map(function(d) { return d.word;})))
        .brushOn(false)
        .yAxisLabel("This is the Good Chart!")
        .dimension(folDimension)
        .group(folGroup)
        .xUnits(dc.units.ordinal)
        .on('renderlet', function(chart) {
            chart.selectAll('rect').on("click", function(d) {
                console.log("click!", d.x);});
            chart.selectAll("g.x text").attr('dx', '-30').attr(
  'dy', '-7').attr('transform', "rotate(90)");
            
        });
      $(document).ready(function() {
                        var t = $('#tabela1').DataTable({"autoWidth": false});
                        var counter = 1;
                            for (var key in data)
                            {
                            var button = '<select name="answer" size="1" id="row-1-office" name="row-1-office"><option>Good</option><option>Bad</option><option>Spam</option>'
                            var aux = t.row.add( [
                                data[String(key)]['word'],
                                data[String(key)]['count']
                            ] ).draw( false );
                            }
                            
                            counter++;
                        });
  chart.render();
  }
    
    
    
function loadGraphBad(data)
  {
  var chart = dc.barChart("#graph2");
  var ndx = crossfilter(data);
  var folDimension = ndx.dimension(function(d) { return d.word;});
  var folGroup = folDimension.group().reduceSum(function(d) { return +d.count;});

  chart
        .width(667)
        .height(580)
        .x(d3.scale.ordinal().domain(data.map(function(d) { return d.word;})))
        .brushOn(false)
        .yAxisLabel("This is the BAD Chart!")
        .dimension(folDimension)
        .group(folGroup)
        .xUnits(dc.units.ordinal)
        .on('renderlet', function(chart) {
            chart.selectAll('rect').on("click", function(d) {
                console.log("click!", d.x);});
            chart.selectAll("g.x text").attr('dx', '-30').attr(
  'dy', '-7').attr('transform', "rotate(90)");
            
        });
      $(document).ready(function() {
                        var t = $('#tabela2').DataTable({"autoWidth": false});
                        var counter = 1;
                            for (var key in data)
                            {
                            var button = '<select name="answer" size="1" id="row-1-office" name="row-1-office"><option>Good</option><option>Bad</option><option>Spam</option>'
                            var aux = t.row.add( [
                                data[String(key)]['word'],
                                data[String(key)]['count']
                            ] ).draw( false );
                            }
                            
                            counter++;
                        });
  chart.render();
  }
    
function loadGraphSpam(data)
  {
  var chart = dc.barChart("#graph3");
  var ndx = crossfilter(data);
  var folDimension = ndx.dimension(function(d) { return d.word;});
  var folGroup = folDimension.group().reduceSum(function(d) { return +d.count;});

  chart
        .width(667)
        .height(580)
        .x(d3.scale.ordinal().domain(data.map(function(d) { return d.word;})))
        .brushOn(false)
        .yAxisLabel("This is the SPAM Chart!")
        .dimension(folDimension)
        .group(folGroup)
        .xUnits(dc.units.ordinal)
        .on('renderlet', function(chart) {
            chart.selectAll('rect').on("click", function(d) {
                console.log("click!", d.x);});
            chart.selectAll("g.x text").attr('dx', '-30').attr(
  'dy', '-7').attr('transform', "rotate(90)");
            
        });
      $(document).ready(function() {
                        var t = $('#tabela3').DataTable({"autoWidth": false});
                        var counter = 1;
                            for (var key in data)
                            {
                            var button = '<select name="answer" size="1" id="row-1-office" name="row-1-office"><option>Good</option><option>Bad</option><option>Spam</option>'
                            var aux = t.row.add( [
                                data[String(key)]['word'],
                                data[String(key)]['count']
                            ] ).draw( false );
                            }
                            
                            counter++;
                        });
  chart.render();
  }
    }

})();