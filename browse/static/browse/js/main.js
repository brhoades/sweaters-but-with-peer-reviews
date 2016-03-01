/* 
 *
 * These are at the top for a reason.
 * Do not move them.
 *
 */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

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

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
        console.log("HELLO!");
    }
  }
);

/*
 *
 * This ends "must be at top" stuff."
 *
 */

// Configure lumx to use csrf
var app = angular.module('lumxWrap', ['lumx']).config(function($httpProvider) {
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller('loginData', function($scope, $http, LxDialogService,
                                     LxNotificationService, $window) {
  $scope.message = "";
  $scope.user = {username: "", password: ""};

  $scope.opendDialog = function(dialogId) {
    LxDialogService.open(dialogId);
  };

  $scope.closingDialog = function() {
  };

  // Someone hit submit
  $scope.submit = function(form) {
    $http.post("/get/login", JSON.stringify(form)).
      success(function(data) {
          if(data["message"] != undefined) {
            $scope.message = data["message"];
          }

          // refresh
          if(data["refresh"]) {
            $scope.closingDialog();
            LxNotificationService.info("Successfully identified.");
            $window.location.href = $window.location.href;
          }
        }).
      error(function() {
        $scope.message = "Network error";
      });
    }
});

app.controller('myCount', function($scope) {
  $scope.count = 0;
});


//This changes the css class based on the size of the window. 
$(window).on('resize', function() {
    if($(window).width() < 1001 ) {
        $('#testing').removeClass('fs-display-4 display-block tc-white-1')
        $('#testing').addClass('fs-display-2 display-block tc-white-1')
    }else {
        $('#testing').removeClass('fs-display-2 display-block tc-white-1')
        $('#testing').addClass('fs-display-4 display-block tc-white-1')
    }
})
