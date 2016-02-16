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


angular.module('lumxWrap').controller('myCount', function($scope) {
  $scope.count = 0;
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
