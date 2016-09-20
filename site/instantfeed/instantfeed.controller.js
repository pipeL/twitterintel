(function () {
    'use strict';

    angular
        .module('app')
        .controller('InstantfeedController', InstantfeedController);

    InstantfeedController.$inject = ['$location', 'GraphsService', '$rootScope'];
    function InstantfeedController($location, GraphsService , $rootScope) {
        var vm = this;
        
        vm.start=start;
        vm.getData = getData;
        vm.changePerfil=changePerfil;
        
        (function initController() {
            // reset login status
            GraphsService.CheckStatus(function(response){
            if($rootScope.globals.currentUser.status=='true'){
                $("#first").hide();
                $("#first1").hide();
                $("#second").show();
                $("#second1").hide();
                $("#third").show();
                alert('Still feeding , check graphs and wait for the end');
            }
            else{
                vm.dataLoading= false;
            }
            
            })
        })();
        
        
        function start() {
            vm.dataLoading = true;
            GraphsService.InstantFeed(vm.track,vm.number,function(response){
                if (response.success) {
                        $("#first").hide();
                        $("#second").show();
                        vm.dataLoading = false;
                    }
                   else {
                        vm.dataLoading = false;
                    }
            })
        };
        /*$( document ).ready(function() {
//grabs the hash tag from the url
var hash = window.location.hash;
//checks whether or not the hash tag is set
if (hash != "") {
//removes all active classes from tabs
$('#tabs li').each(function() {
$(this).removeClass('active');
});
$('#myTabContent div').each(function() {
  $(this).removeClass('in active');
});
//this will add the active class on the hashtagged value
var link = "";
$('#tabs li').each(function() {
  link = $(this).find('a').attr('href');
  if (link == hash) {
    $(this).addClass('active');
  }
});
$('#myTabContent div').each(function() {

  link = $(this).attr('id');
  if ('#'+link == hash) {

    $(this).addClass('in active');
  }
});
}
});*/
        function getData(data){
            GraphsService.GetData(function(response){
                vm.dataLoading = true;
                var table =  $('#tabela').DataTable();
                var table1 = $('#tabela1').DataTable();
                var table2 = $('#tabela2').DataTable();
                var table3 = $('#tabela3').DataTable();
 
            table
                .clear()
                .destroy();
            table1
                .clear()
                .destroy();
            table2
                .clear()
                .destroy();
            table3
                .clear()
                .destroy();
                var tweets = new Array();
                var word = new Array();
                var twoword = new Array();
                var threeword = new Array();
                if (response.success) {
                    vm.dataLoading = false;
                    for (var key in $rootScope.data['tweet'])
                    {
                        tweets.push($rootScope.data['tweet'][String(key)])
                    }
                    for (var key in $rootScope.data['word'])
                    {
                        word.push($rootScope.data['word'][String(key)])
                    }
                    for (var key in $rootScope.data['twoword'])
                    {
                        twoword.push($rootScope.data['twoword'][String(key)])
                    }
                    for (var key in $rootScope.data['threeword'])
                    {
                        threeword.push($rootScope.data['threeword'][String(key)])
                    }
                    loadTweets(tweets);
                    loadWord(word);
                    loadTwoWord(twoword);
                    loadThreeWord(threeword);
                    $("#third").show();
                    
                }
                else{
                    alert(response);
                }
            })
            vm.dataLoading=false;
        }
function loadTweets(data){
  $(document).ready(function() {
                        var t = $('#tabela').DataTable();
                        var counter = 1;
                            for (var key in data)
                            {
                            var button = '<select name="answer" size="1" id="row-1-office" name="row-1-office"><option>Good</option><option>Bad</option><option>Spam</option>'
                            var aux = t.row.add( [
                                String(data[key])
                            ] ).draw( false );
                            }
                            
                            counter++;
                        });
  }
 function loadWord(data)
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
        .yAxisLabel("This is the Word Chart!")
        .dimension(folDimension)
        .group(folGroup)
        .xUnits(dc.units.ordinal)
        .on('renderlet', function(chart) {
            chart.selectAll('rect').on("click", function(d) {
                console.log("click!", d.x);
            chart.selectAll("g.x text").attr('dx', '-30').attr(
  'dy', '-7').attr('transform', "rotate(90)");
            });
        });
      $(document).ready(function() {
                        var t = $('#tabela1').DataTable();
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
    
    
    
function loadTwoWord(data)
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
        .yAxisLabel("This is the Two Word Chart!")
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
                        var t = $('#tabela2').DataTable();
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
        
        
function changePerfil()
  {
      if ($("#first").is(":visible"))
          {
              $("#first").hide();
              $("#first1").hide();
              $("#second").show();
              $("#second1").show();
              $("#third").show();
          }
      else{
          $("#first").show();
          $("#first1").show();
          $("#second").hide();
          $("#second1").hide();
          $("#third").hide();
      }
  }
function loadThreeWord(data)
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
        .yAxisLabel("This is the Three Word Chart!")
        .dimension(folDimension)
        .group(folGroup)
        .xUnits(dc.units.ordinal)
        .on('renderlet', function(chart) {
            chart.selectAll('rect').on("click", function(d) {
                console.log("click!", d.x);
            });
            chart.selectAll("g.x text").attr('dx', '-30').attr(
  'dy', '-7').attr('transform', "rotate(90)");
        });
      $(document).ready(function() {
                        var t = $('#tabela3').DataTable();
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