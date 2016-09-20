(function () {
    'use strict';

    angular
        .module('app')
        .controller('EvaluationController', EvaluationController);

    EvaluationController.$inject = ['$location', 'GraphsService', '$rootScope'];
    function EvaluationController($location, GraphsService , $rootScope) {
        var vm = this;

        vm.getalltweets= getalltweets;
        vm.startFeed = startFeed;
        vm.auxsenddata = auxsenddata;

        function getalltweets() {
            
            GraphsService.GetEvaluation(function(response){
                vm.dataLoading = true;
                var tweets = $rootScope.tweets;
                if (response.success) {
                        var button = '<tr><td><select class="form-control custom"><option>Good</option><option>Bad</option><option>Spam</option></select></ul></div></td>';
                        for(var key in tweets){

                            $('[name=unico]').append(button + '<td name="tweet"><h3>' + String(tweets[String(key)])  + '</h3></td></tr>');

                            //$(".tabela").append('<select class="' + String(key) + '">' + "<option>Good</option><option>Bad</option><option>Spam</option></select>");
                        }
                        
                        
                    vm.dataLoading=false;
                            $("#second").show()
                    }              
                   else {
                        alert('ERROR');
                        vm.dataLoading = false;
                    }
                
            })
        }
                              
                              
        
        
        function auxsenddata(data){
            GraphsService.SendData(data,function(response){
                vm.dataLoading = true;
                if (response.success) {
                    vm.dataLoading = false;
                    $location.path('/topwordsgraphs');
                }
                else{
                    alert(response);
                }
            })
                                   
                                   }
            
        
        function startFeed()
        {
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