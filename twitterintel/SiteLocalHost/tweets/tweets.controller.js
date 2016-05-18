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
            
            GraphsService.GetAllTweets(function(response){
                vm.dataLoading = true;
                var good = $rootScope.GoodData;
                var bad = $rootScope.BadData;
                var spam = $rootScope.SpamData;
                if (response.success) {
                        /*var table = $("#tabela");
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
                        $(document).ready(function() {
                            $('#tabela').DataTable( {
                                "paging":   false,
                                "ordering": false,
                                "info":     false
                            } );
                        } );*/
                        
                        $(document).ready(function() {
                        var t = $('#tabela').DataTable({"autoWidth": false});
                        var counter = 1;
                            for (var key in good)
                            {
                            var button = '<select name="answer" size="1" id="row-1-office" name="row-1-office"><option>Good</option><option>Bad</option><option>Spam</option>'
                            var aux = t.row.add( [
                                button,
                                good[key]['tweet']
                            ] ).draw( false );
                            }
                            for (var key in bad)
                            {
                            var button = '<select name="answer" size="1" id="row-1-office" name="row-1-office"><option>Bad</option><option>Good</option><option>Spam</option>'
                            var aux=t.row.add( [
                                button,
                                bad[key]['tweet']
                            ] ).draw( false );
                            }
                            
                            counter++;
                        });
                        
                        
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
        var count = 0;
            $("#tabela").find("td").each(function(index){
                if(index%2 != 0 || index==0){
                array[count]={}
                array[count]['tweet']=$(this).text();
                count++;
                }
            });
            count = 0;
            $("#tabela").find("[name=answer]").each(function(index){
               array[count]['answer']=$(this).find('option:selected').text();
               count++;
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