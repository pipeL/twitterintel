(function () {
    'use strict';

    angular
        .module('app')
        .controller('RankingwordsController', RankingwordsController);

    RankingwordsController.$inject = ['$location', 'GraphsService', '$rootScope', '$scope'];
    function RankingwordsController($location, GraphsService , $rootScope , $scope) {
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
        
      $scope.cbSelected = function () {
      if ($scope.myCheckbox) {
            $("#saveText").show();
      } else {
        $scope.text1.hide();
      }
    }
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
        var table = $("#tabela").DataTable();
        table.rows().every( function ( rowIdx, tableLoop, rowLoop ) {
            var data = this.data();
            var aux = table.row(this).node();
            var aux2 = $(aux).find("[name=prob]");
            var aux3 = $(aux).find("[name=type]");
            var aux4 = $(aux).find("[name=word]");
            var prob = $(aux2).val();
            var type = $(aux3).text();
            var word= $(aux4).text();
            if (type=='Bad')
                {
                    arrayBad[word] =prob
                }
            if (type=='Good')
                {
                    arrayGood[word] =prob
                }
            if (type=='Spam')
                {
                    arraySpam[word] =prob
                }
            
    // ... do something with data(), or this.node(), etc
        } );
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
                var table = $("#tabela").DataTable();
        table.rows().every( function ( rowIdx, tableLoop, rowLoop ) {
            var data = this.data();
            var aux = table.row(this).node();
            var aux2 = $(aux).find("[name=prob]");
            var aux3 = $(aux).find("[name=type]");
            var aux4 = $(aux).find("[name=word]");
            var prob = $(aux2).val();
            var type = $(aux3).text();
            var word= $(aux4).text();
            if (type=='Bad')
                {
                    arrayBad[word] =prob
                }
            if (type=='Good')
                {
                    arrayGood[word] =prob
                }
            if (type=='Spam')
                {
                    arraySpam[word] =prob
                }
            
    // ... do something with data(), or this.node(), etc
        } );
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
        if ($scope.myCheckbox) {
            alert($("#saveText").text())
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
                        /*var button = '<tr name="row"><td><h3 name ="type">Good</h3></td><td><textarea name="prob" style="width: 100%; height: 100%; border:None">';
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
                        }*/
                        $(document).ready(function() {
                        var t = $('#tabela').DataTable();
                        var counter = 1;
                            for (var key in good)
                            {
                            var button = '<select name="answer" size="1" id="row-1-office" name="row-1-office"><option>Good</option><option>Bad</option><option>Spam</option>'
                            var aux = t.row.add( [
                                '<h3 name ="type">Good</h3>',
                                '<textarea name="prob" style="width: 100%; height: 100%; border:None">' + good[String(key)] + '</textarea>',
                                '<h3 name="word">' + String(key) + '</h3>'
                            ] ).draw( false );
                            }
                            for (var key in bad)
                            {
                            var button = '<select name="answer" size="1" id="row-1-office" name="row-1-office"><option>Bad</option><option>Bad</option><option>Spam</option>'
                            var aux = t.row.add( [
                                '<h3 name ="type">Bad</h3>',
                                '<textarea name="prob" style="width: 100%; height: 100%; border:None">' + bad[String(key)] + '</textarea>',
                                '<h3 name="word">' + String(key) + '</h3>'
                            ] ).draw( false );
                            }
                            
                            counter++;
                        });
                        
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
                        /*var button = '<tr name="row"><td><h3 name ="type">Good</h3></td><td><textarea name="prob" style="width: 100%; height: 100%; border:None">';
                        for(var key in good){

                            $('[name=unico]').append(button + good[String(key)] + '</textarea></ul></div></td>' + '<td><h3 name="word">' + String(key) + '</h3></td></tr>');

                            //$(".tabela").append('<select class="' + String(key) + '">' + "<option>Good</option><option>Bad</option><option>Spam</option></select>");
                        }
                        button = '<tr name="row"><td><h3 name ="type">Bad</h3></td><td><textarea name="prob" style="width: 100%; height: 100%; border:None">';
                        for(var key in bad){

                            $('[name=unico]').append(button + bad[String(key)] + '</textarea></ul></div></td>' + '<td><h3 name="word">' + String(key) + '</h3></td></tr>');

                            //$(".tabela").append('<select class="' + String(key) + '">' + "<option>Good</option><option>Bad</option><option>Spam</option></select>");
                        }*/
                        $(document).ready(function() {
                        var t = $('#tabela').DataTable();
                        var counter = 1;
                            for (var key in good)
                            {
                            var button = '<select name="answer" size="1" id="row-1-office" name="row-1-office"><option>Good</option><option>Bad</option><option>Spam</option>'
                            var aux = t.row.add( [
                                '<h3 name ="type">Good</h3>',
                                '<textarea name="prob" style="width: 100%; height: 100%; border:None">' + good[String(key)] + '</textarea>',
                                '<h3 name="word">' + String(key) + '</h3>'
                            ] ).draw( false );
                            }
                            for (var key in bad)
                            {
                            var button = '<select name="answer" size="1" id="row-1-office" name="row-1-office"><option>Bad</option><option>Bad</option><option>Spam</option>'
                            var aux = t.row.add( [
                                '<h3 name ="type">Good</h3>',
                                '<textarea name="prob" style="width: 100%; height: 100%; border:None">' + bad[String(key)] + '</textarea>',
                                '<h3 name="word">' + String(key) + '</h3>'
                            ] ).draw( false );
                            }
                            
                            counter++;
                        });
                        
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