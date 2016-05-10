(function () {
    'use strict';

    angular
        .module('app')
        .factory('GraphsService', GraphsService);

    GraphsService.$inject = ['$rootScope' , '$q'];
    function GraphsService($rootScope, $q) {
        var service = {};

        service.Success = Success;
        service.Error = Error;
        service.Learning = Learning;
        service.Results = Results;
        service.GetAllProb = GetAllProb;
        service.SendData = SendData;
        service.SendDataPerce = SendDataPerce;
        service.GetAllGraphs= GetAllGraphs;
        service.GetAllGraphs2= GetAllGraphs2;
        service.GetAllGraphs3= GetAllGraphs3;
        service.GetAllTweets= GetAllTweets;
        service.GetAllInfo =GetAllInfo;
        service.GetProbPerce=GetProbPerce;
        service.CheckStatus=CheckStatus;
        return service;

        function Learning(track , number , callback) {
           var send = new Array()
           var data= new Array();
            var response ;
            var deferred = $q.defer();
           send[0] = track;
           send[1] = number;
           send[2]= $rootScope.globals.currentUser.id;
           $.ajax({
                  type: "GET",
                  crossDomain: true,
                  data: {id:JSON.stringify(send)},
                  url: "http://localhost:7000/Learning",
                  dataType: "json",
                  success: function(result){
                    if (result['0']=='false')
                    {
                        alert('Feed didnt terminate well, maybe not a usually keyword');
                        response = {success : false};
                        $rootScope.$apply(function(){
                            callback(response);
                        });
                    }
                    else{
                        $rootScope.tweets=result;
                        response = {success : true};
                        $rootScope.$apply(function(){
                            callback(response);
                        });
                    }
                  },
                  error : function(e){
                        alert(e);
                  }
          })
           return deferred.promise;
          } 
        
        
        
        function Results(array, callback){
            var response;
        $.ajax({
          type: "GET",
          crossDomain: true,
          data: {id:JSON.stringify(array)},     // content type sent to server
          dataType: "json",
          url: "http://localhost:7000/Results",
          success: function(result){
                 response = {success : true}
                    $rootScope.$apply(function(){
                        callback(response);
                    });
          },
          error : function(e){
                response = {success : true}
                    $rootScope.$apply(function(){
                        callback(response);
                    });
          }
        })
        }
        
        
        function CheckStatus(callback){
            var response;
            var user=$rootScope.globals.currentUser.id;
        $.ajax({
          type: "GET",
          crossDomain: true,
          data: {id:user},     // content type sent to server
          dataType: "json",
          url: "http://localhost:7000/CheckStatus",
          success: function(result){
                 $rootScope.globals.currentUser.status = result['0']; 
                 response = {success : true}
                    $rootScope.$apply(function(){
                        callback(response);
                    });
          },
          error : function(e){
                response = {success : false}
                    $rootScope.$apply(function(){
                        callback(response);
                    });
          }
        })
        }
        
        function GetAllProb(callback){
           var response = {success : false};
           var deferred = $q.defer();
           var user = $rootScope.globals.currentUser.id;
           var goodservice=$.ajax({
                  type: "GET",
                  crossDomain: true,
                  data:{id: user},
                  url: "http://localhost:7000/getWordProbGood",
                  dataType: "json",
                  success: function(result){
                         response = {success : true};
                         $rootScope.GoodProb=result; 
                  },
                  error : function(e){
                      
                        response = {success : false};
                  }
          })
           var badservice=$.ajax({

                  type: "GET",
                  crossDomain: true,
                  data:{id: user},
                  url: "http://localhost:7000/getWordProbBad",
                  dataType: "json",
                  success: function(result){
                         response = {success : true};
                         $rootScope.BadProb=result; 
                  },
                  error : function(e){
                        response = {success : false};
                  }
          })
           var spamservice=$.ajax({

                  type: "GET",
                  crossDomain: true,
                  data:{id: user},
                  url: "http://localhost:7000/getWordProbSpam",
                  dataType: "json",
                  success: function(result){
                         response = {success : true};
                         $rootScope.SpamProb=result; 
                  },
                  error : function(e){
                        response = {success : false};
                  }
          })
           
            $.when(goodservice,badservice,spamservice).done(function(goodservice,badservice,spamservice){
                                                            callback(response);
                                                            })
        }
        function SendData(data){
            var response;
            $.ajax({
          type: "GET",
          crossDomain: true,
          data: {id:JSON.stringify(data)},     // content type sent to server
          dataType: "json",
          url: "http://localhost:7000/StartFeedModifie",
          success: function(result){
                if(result['0']=='true'){
                    alert('Feed is Done');
                    $rootScope.globals.currentUser.status = false;
                }
                else{
                    alert('Feed didnt terminate nicely');
                    $rootScope.globals.currentUser.status = false;
                }
                        
                                    
          },
          error : function(e){ response = {success : true};
          }
        })
        }
        
        
        function SendDataPerce(data,callback){
            var response;
            $.ajax({
          type: "GET",
          crossDomain: true,
          data: {id:JSON.stringify(data)},     // content type sent to server
          dataType: "json",
          url: "http://localhost:7000/StartFeedPerceptron",
          success: function(result){
                if(result['0']=='true'){
                    alert('Feed is Done');
                    $rootScope.globals.currentUser.status = false;
                }
                                    
          },
          error : function(e){ ralert('Feed didnt terminate nicely');
                    $rootScope.globals.currentUser.status = false;
          }
        })
        }
        
        function GetAllGraphs(callback){
            var response = {success : false};
            var deferred = $q.defer();
            var data= new Array()
            var datagood= new Array();
            var databad= new Array();
            var dataspam= new Array();
            var user = $rootScope.globals.currentUser.id;
          var totalgraph= $.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getTotal",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 data.push(aux);
                 }
                 response = {success : true};
                 $rootScope.Total=data

          },
          error : function(e){
                response = {success : false , message: "ERRO LOGIN"};
          }
        })

        var goodgraph=$.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getTopWordGood",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 datagood.push(aux);
                 }
                 response = {success : true};
                 $rootScope.GoodData=datagood;

          },
          error : function(e){
                response = {success : false};
          }
        })
        var badgraph=$.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getTopWordBad",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 databad.push(aux);
                 }
                 response = {success : true};
                 $rootScope.BadData=databad;

          },
          error : function(e){
                response = {success : false};
          }
        })
        var spamgraph=$.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getTopWordSpam",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 databad.push(aux);
                 }
                 response = {success : true};
                 $rootScope.SpamData=dataspam;

          },
          error : function(e){
                response = {success : false};
          }
        })
           
        $.when(totalgraph,goodgraph,badgraph,spamgraph).done(function(totalgraph,goodgraph,badgraph,spamgraph){
                                                            callback(response);
                                                            })
        }
        
        function GetAllGraphs2(callback){
            var response = {success : false};
            var deferred = $q.defer();
            var data= new Array()
            var datagood= new Array();
            var databad= new Array();
            var dataspam= new Array();
            var user = $rootScope.globals.currentUser.id;
          var totalgraph= $.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getTotal",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 data.push(aux);
                 }
                 response = {success : true};
                 $rootScope.Total=data

          },
          error : function(e){
                response = {success : false , message: "ERRO LOGIN"};
          }
        })

        var goodgraph=$.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getTopTwoWordGood",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 datagood.push(aux);
                 }
                 response = {success : true};
                 $rootScope.GoodData=datagood;

          },
          error : function(e){
                response = {success : false};
          }
        })
        var badgraph=$.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getTopTwoWordBad",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 databad.push(aux);
                 }
                 response = {success : true};
                 $rootScope.BadData=databad;

          },
          error : function(e){
                response = {success : false};
          }
        })
        var spamgraph=$.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getTopTwoWordSpam",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 databad.push(aux);
                 }
                 response = {success : true};
                 $rootScope.SpamData=dataspam;

          },
          error : function(e){
                response = {success : false};
          }
        })
           
        $.when(totalgraph,goodgraph,badgraph,spamgraph).done(function(totalgraph,goodgraph,badgraph,spamgraph){
                                                            callback(response);
                                                            })
        }
        
        function GetAllGraphs3(callback){
            var response = {success : false};
            var deferred = $q.defer();
            var data= new Array()
            var datagood= new Array();
            var databad= new Array();
            var dataspam= new Array();
            var user = $rootScope.globals.currentUser.id;
          var totalgraph= $.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getTotal",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 data.push(aux);
                 }
                 response = {success : true};
                 $rootScope.Total=data

          },
          error : function(e){
                response = {success : false , message: "ERRO LOGIN"};
          }
        })

        var goodgraph=$.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getTopThreeWordGood",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 datagood.push(aux);
                 }
                 response = {success : true};
                 $rootScope.GoodData=datagood;

          },
          error : function(e){
                response = {success : false};
          }
        })
        var badgraph=$.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getTopThreeWordBad",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 databad.push(aux);
                 }
                 response = {success : true};
                 $rootScope.BadData=databad;

          },
          error : function(e){
                response = {success : false};
          }
        })
        var spamgraph=$.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getTopThreeWordSpam",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 databad.push(aux);
                 }
                 response = {success : true};
                 $rootScope.SpamData=dataspam;

          },
          error : function(e){
                response = {success : false};
          }
        })
           
        $.when(totalgraph,goodgraph,badgraph,spamgraph).done(function(totalgraph,goodgraph,badgraph,spamgraph){
                                                            callback(response);
                                                            })
        }
        
        
        function GetAllTweets(callback){
            var response = {success : false};
            var deferred = $q.defer();
            var data= new Array()
            var datagood= new Array();
            var databad= new Array();
            var dataspam= new Array();
            var user = $rootScope.globals.currentUser.id;
            
           var tweetsgood= $.ajax({
       
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getTweetsBad",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 databad.push(aux);
                 }
                 response = {success : true};
                 $rootScope.BadData=databad;
          },
          error : function(e){
                response = {success : false};
          }
  })
   var tweetsbad = $.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getTweetsGood",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 datagood.push(aux);
                 }
                 response = {success : true};
                 $rootScope.GoodData=datagood;

          },
          error : function(e){
                response = {success : false};
          }
       
  })
   var tweetsspam = $.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getTweetsSpam",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 data.push(aux);
                 }
                 response = {success : true};
                 $rootScope.SpamData=dataspam;

          },
          error : function(e){
                response = {success : false};
          }
  })
   $.when(tweetsgood,tweetsbad,tweetsspam).done(function(tweetsgood,tweetsbad,tweetsspam){
                                                            callback(response);
                                                            })
  }


        
        
        
function GetProbPerce(callback){
            var response = {success : false};
            var deferred = $q.defer();
            var datagood= new Array();
            var databad= new Array();
            var user = $rootScope.globals.currentUser.id;
            
           var GetProbGood= $.ajax({
       
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getWordProbPerceptronGood",
          dataType: "json",
          success: function(result){
                 response = {success : true};
                 $rootScope.GoodProb=result;
                 
          },
          error : function(e){
                response = {success : false};
          }
  })
   var GetProbBad = $.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getWordProbPerceptronBad",
          dataType: "json",
          success: function(result){
                 response = {success : true};
                 $rootScope.BadProb=result;

          },
          error : function(e){
                response = {success : false};
          }
       
  })
   $.when(GetProbBad,GetProbGood).done(function(GetProbBad,GetProbGood){
                                                            callback(response);
                                                            })
  }
        
        
function GetAllInfo(callback){
    var response = {success : false};
    var datagood= new Array();
    var databad = new Array();
    var user = $rootScope.globals.currentUser.id;
    
    var goodtweets =$.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getInfoTweetsGood",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 datagood.push(aux);
                 }
                 response = {success : true};
                 $rootScope.datagood=datagood;
          },
          error : function(e){
                alert(e)
          }
  })
    var badtweets = $.ajax({
          type: "GET",
          crossDomain: true,
          data:{id: user},
          url: "http://localhost:7000/getInfoTweetsBad",
          dataType: "json",
          success: function(result){
                 for(var key in result){
                 var aux = result[String(key)];
                 databad.push(aux);
                 }
                 response = {success : true};
                 $rootScope.databad=databad;
          },
          error : function(e){
                alert(e)
          }
  })
    $.when(badtweets,goodtweets).done(function(badtweets,goodtweets){
                                                            callback(response);
                                                            })
  }
        
        
        
        function Success(message, keepAfterLocationChange) {
            $rootScope.flash = {
                message: message,
                type: 'success', 
                keepAfterLocationChange: keepAfterLocationChange
            };
        }

        function Error(message, keepAfterLocationChange) {
            $rootScope.flash = {
                message: message,
                type: 'error',
                keepAfterLocationChange: keepAfterLocationChange
            };
        }
    }
})();