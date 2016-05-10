(function () {
    'use strict';

    angular
        .module('app')
        .controller('RankingwordsController', RankingwordsController);

    RankingwordsController.$inject = ['$location', 'GraphsService', '$rootScope'];
    function RankingwordsController($location, GraphsService , $rootScope) {
        var vm = this;

        vm.getallprob= getallprob;
        vm.submitData = submitData;
        vm.auxsenddata = auxsenddata;
        
        (function initController() {
            // reset login status
            GraphsService.CheckStatus(function(response){
                                      if($rootScope.globals.currentUser.status=='true'){
                alert('Still feeding , you can change probability but you cant insert');
            }
            else{
                vm.dataLoading= false;
            }
            
                                      })
        })();
        
        function submitData()
        {
        var arrayGood = {};
        var arrayBad = {};
        var arraySpam = {};
        var toSend = {};
        vm.dataLoading = true;
        var aux = $rootScope.globals.currentUser.intel;
        if(aux == 'naive')
        {
        $("#tabela").find('[name=row]').each(function(index){
        if($(this).find('[name=type]').text() == 'Good')
        {
            arrayGood[$(this).find('[name=word]').text()] =$(this).find('[name=prob]').val();
        }
        if($(this).find('[name=type]').text() == 'Bad')
        {
            arrayBad[$(this).find('[name=word]').text()] =$(this).find('[name=prob]').val();
        }
        if($(this).find('[name=type]').text() == 'Spam')
        {
            arraySpam[$(this).find('[name=word]').text()] =$(this).find('[name=prob]').val();
        }
        })
        toSend[0]=vm.track;
        toSend[1]=vm.number;
        toSend[2]=arrayGood;
        toSend[3]=arrayBad;
        toSend[4]=arraySpam;
        toSend[5]=$rootScope.globals.currentUser.id;
        if ($rootScope.globals.currentUser.status=='true')
            {
                vm.dataLoading = true;
            }
        else{
            auxsenddata(toSend);
            vm.dataLoading = false;
        }
        }
        else
            {
                $("#tabela").find('[name=row]').each(function(index){
        if($(this).find('[name=type]').text() == 'Good')
        {
            arrayGood[$(this).find('[name=word]').text()] =$(this).find('[name=prob]').val();
        }
        if($(this).find('[name=type]').text() == 'Bad')
        {
            arrayBad[$(this).find('[name=word]').text()] =$(this).find('[name=prob]').val();
        }
        if($(this).find('[name=type]').text() == 'Spam')
        {
            arraySpam[$(this).find('[name=word]').text()] =$(this).find('[name=prob]').val();
        }
        })
        toSend[0]=vm.track;
        toSend[1]=vm.number;
        toSend[2]=arrayGood;
        toSend[3]=arrayBad;
        toSend[4]=$rootScope.globals.currentUser.id;
        if ($rootScope.globals.currentUser.status=='true')
            {
                vm.dataLoading = true;
            }
        else{
            auxsenddata(toSend);
            vm.dataLoading = false;
        }
        
        
            }
        
    }

        function getallprob() {
            vm.dataLoading = true;
            var aux = $rootScope.globals.currentUser.intel;
            if (aux == 'naive')
                {
                    GraphsService.GetAllProb(function(response){
                var good = $rootScope.GoodProb;
                var bad = $rootScope.BadProb;
                var spam = $rootScope.SpamProb;
                if (response.success) {
                        var button = '<tr name="row"><td><h3 name ="type">Good</h3></td><td><textarea name="prob" style="width: 100%; height: 100%; border:None">';
                        for(var key in good){

                            $('[name=unico]').append(button + good[String(key)] + '</textarea></ul></div></td>' + '<td><h3 name="word">' + String(key) + '</h3></td></tr>');

                            //$(".tabela").append('<select class="' + String(key) + '">' + "<option>Good</option><option>Bad</option><option>Spam</option></select>");
                        }
                        button = '<tr name="row"><td><h3 name ="type">Bad</h3></td><td><textarea name="prob" style="width: 100%; height: 100%; border:None">';
                        for(var key in bad){

                            $('[name=unico]').append(button + bad[String(key)] + '</textarea></ul></div></td>' + '<td><h3 name="word">' + String(key) + '</h3></td></tr>');

                            //$(".tabela").append('<select class="' + String(key) + '">' + "<option>Good</option><option>Bad</option><option>Spam</option></select>");
                        }
                        var button = '<tr name="row"><td><h3 name ="type">Spam</h3></td><td><textarea name="prob" style="width: 100%; height: 100%; border:None">';
                        for(var key in spam){

                            $('[name=unico]').append(button + spam[String(key)] + '</textarea></ul></div></td>' + '<td><h3  name="word">' + String(key) + '</h3></td></tr>');

                            //$(".tabela").append('<select class="' + String(key) + '">' + "<option>Good</option><option>Bad</option><option>Spam</option></select>");
                        }
                        
                        $("#second").show();
                        vm.dataLoading = false;
                    }
                   else {
                     
                            alert('ERROR');
                            vm.dataLoading = false;
                    }
                    })
                                             }
                else
                {
            GraphsService.GetProbPerce(function(response){
                var good = $rootScope.GoodProb;
                var bad = $rootScope.BadProb;
                if (response.success) {
                        var button = '<tr name="row"><td><h3 name ="type">Good</h3></td><td><textarea name="prob" style="width: 100%; height: 100%; border:None">';
                        for(var key in good){

                            $('[name=unico]').append(button + good[String(key)] + '</textarea></ul></div></td>' + '<td><h3 name="word">' + String(key) + '</h3></td></tr>');

                            //$(".tabela").append('<select class="' + String(key) + '">' + "<option>Good</option><option>Bad</option><option>Spam</option></select>");
                        }
                        button = '<tr name="row"><td><h3 name ="type">Bad</h3></td><td><textarea name="prob" style="width: 100%; height: 100%; border:None">';
                        for(var key in bad){

                            $('[name=unico]').append(button + bad[String(key)] + '</textarea></ul></div></td>' + '<td><h3 name="word">' + String(key) + '</h3></td></tr>');

                            //$(".tabela").append('<select class="' + String(key) + '">' + "<option>Good</option><option>Bad</option><option>Spam</option></select>");
                        }
                        
                        $("#second").show();
                        vm.dataLoading = false;
                    }
                   else {
                        alert('ERROR');
                        vm.dataLoading = false;
                    }
                })
                }
            vm.dataLoading=false;
        }
        
        
        function auxsenddata(data){
            if($rootScope.globals.currentUser.intel == 'naive')
                {
                    GraphsService.SendData(data);
                    $location.path('/topwordsgraphs');
                }
            else
                {
                   GraphsService.SendDataPerce(data)
                   $location.path('/topwordsgraphs');
                } 
                }
    }
            

})();