/*var app = angular.module('myApp', []);

app.controller('test', function($scope, LxDialogService, LxNotificationService) {

    $scope.opendDialog = function(dialogId)
    {
        LxDialogService.open(dialogId);
    };

    $scope.closingDialog = function()
    {
        LxNotificationService.info('Dialog closed!');
    };
});*/


angular.module('testApp', [])
.controller('myCount', function($scope) {
  $scope.count = 0;
});
