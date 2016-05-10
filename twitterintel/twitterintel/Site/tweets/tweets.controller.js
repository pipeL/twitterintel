(function () {
    'use strict';

    angular
        .module('app')
        .controller('TweetsController', TweetsController);

    TweetsController.$inject = ['$location', 'GraphsService', '$rootScope'];
    function TweetsController($location, GraphsService , $rootScope) {
        var vm = this;

        vm.getalltweets= getalltweets;
        vm.startFeed = startFeed;
        vm.auxsenddata = auxsenddata;

        function getalltweets() {
            vm.dataLoading = true;
            GraphsService.GetAllTweets(function(response){
                var good = $rootScope.GoodData;
                var bad = $rootScope.BadData;
                var spam = $rootScope.SpamData;
                if (response.success) {
                        var table = $("#tabela");
                        var button = '<tr><td><select class="form-control custom"><option>Good</option><option>Bad</option><option>Spam</option></select></ul></div></td>';
                        for (var key in good)
                        {
                            table.append(button+ '<td name="tweet"><h3>' + good[key]['tweet']  + '</h3></td></tr>'  );
                        }
                    
                        var table = $("#tabela");
                        var button = '<tr><td><select class="form-control custom"><option>Bad</option><option>Good</option><option>Spam</option></select></ul></div></td>';
                        for (var key in bad)
                        {
                            table.append(button+ '<td name="tweet"><h3>' + bad[key]['tweet']  + '</h3></td></tr>'  );
                        }  
              
                        var table = $("#tabela");
                        var button = '<tr><td><select class="form-control custom"><option>Spam</option><option>Good</option><option>Bad</option></select></ul></div></td>';
                        for (var key in spam)
                        {
                            table.append(button+ '<td name="tweet"><h3>' + spam[key]['tweet']  + '</h3></td></tr>'  );
                        }
                        vm.dataLoading =false;
                    }                
                   else {
                        alert('ERROR');
                        vm.dataLoading = false;
                    }
                
            })
            vm.dataLoading=false;
        };
        
        
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