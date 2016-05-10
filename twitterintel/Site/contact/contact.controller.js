(function () {
    'use strict';

    angular
        .module('app')
        .controller('ContactController', ContactController);

    ContactController.$inject = ['UserService', '$scope'];
    function ContactController(UserService, $scope) {
    $scope.result = 'hidden'
    $scope.resultMessage;
    $scope.formData; //formData is an object holding the name, email, subject, and message
    $scope.submitButtonDisabled = false;
    $scope.submitted = false; //used so that form errors are shown only after the form has been submitted
    $scope.submit = function(contactform) {
        $scope.submitted = true;
        $scope.submitButtonDisabled = true;
        if (contactform.$valid) {
            var send = new Array();
            send[0]=$scope.formData.inputEmail;
            send[1]=$scope.formData.inputMessage;
            send[2]=$scope.formData.inputName;
            send[3]=$scope.formData.inputSubject;
            $.ajax({
                method  : 'GET',
                url     : "http://31.193.129.198:7000/Contact",
                crossDomain: true,
                data    : {id:JSON.stringify(send)},  //param method from jQuery
                dataType: "json",
            }).success(function(data){
                console.log(data);
                if (data.success) { //success comes from the return json object
                    $scope.submitButtonDisabled = true;
                    $scope.resultMessage = data.message;
                    $scope.result='bg-success';
                } else {
                    $scope.submitButtonDisabled = false;
                    $scope.resultMessage = data.message;
                    $scope.result='bg-danger';
                }
            });
        } else {
            $scope.submitButtonDisabled = false;
            $scope.resultMessage = 'Failed <img src="http://www.chaosm.net/blog/wp-includes/images/smilies/icon_sad.gif" alt=":(" class="wp-smiley">  Please fill out all the fields.';
            $scope.result='bg-danger';
        }
    }
    }
})();

