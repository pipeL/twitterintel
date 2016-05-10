(function () {
    'use strict';

    angular
        .module('app')
        .controller('StartController', StartController);

    StartController.$inject = ['$location', 'GraphsService', '$rootScope'];
    function StartController($location, GraphsService , $rootScope) {
        var vm = this;
        vm.start = start;
        vm.results= results;
        
        
        (function initController() {
            // reset login status
            GraphsService.CheckStatus(function(response){
            if($rootScope.globals.currentUser.status=='true'){
                vm.dataLoading = true;
                alert('Still feeding , check graphs and wait for the end');
            }
            else{
                vm.dataLoading= false;
            }
            
            })
        })();

        function start() {
            vm.dataLoading = true;
            GraphsService.Learning(vm.track,vm.number,function(response){
                var tweets = $rootScope.tweets;
                if (response.success) {
                        var button = '<tr><td><select class="form-control custom"><option>Good</option><option>Bad</option><option>Spam</option></select></ul></div></td>';
                        for(var key in tweets){

                            $('[name=unico]').append(button + '<td name="tweet"><h3>' + String(tweets[String(key)])  + '</h3></td></tr>');

                            //$(".tabela").append('<select class="' + String(key) + '">' + "<option>Good</option><option>Bad</option><option>Spam</option></select>");
                        }
                        $("#first").hide()
                        $("#second").show()
                        vm.dataLoading = false;
                    }
                   else {
                        vm.dataLoading = false;
                    }
            })
        };
        
        function results(){
            vm.dataLoading = true;
            
            var array = {}
            $("#tabela").find('[name=tweet]').each(function(index){
                array[index]={}
                array[index]['tweet']=$(this).text();
            });
            $("select").each(function(index){
               array[index]['answer']=$(this).find('option:selected').text(); 
            });
            array[0]['user']=$rootScope.globals.currentUser.id;
            GraphsService.Results(array, function(response)
            {
                if (response.success) {
                        vm.dataLoading = false;
                        $location.path('/rankingwords');
                    } else {
                        alert(response);
                        vm.dataLoading = false;
                    }
            })
        }
    }

})();