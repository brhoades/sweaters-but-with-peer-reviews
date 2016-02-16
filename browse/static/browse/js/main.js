var myAppModule = angular.module('myApp', []);

myAppModule.controller(function ($scope, LxDialogService, LxNotificationService) {

    $scope.opendDialog = function(dialogId)
    {
        LxDialogService.open(dialogId);
    };

    $scope.closingDialog = function()
    {
        LxNotificationService.info('Dialog closed!');
    };
} );