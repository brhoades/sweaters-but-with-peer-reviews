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

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
  }
);

angular.module('lumxWrap').controller('getReviewForm', function($scope, $http) {
  $scope.formData = {};
  
  $scope.description = {
    update: function(newVal) {
      $scope.formData["text"] = newVal;
    }
  };

  $scope.ajax = {
      selected: '',
      list: [],
      update: function(newFilter, oldFilter, subtext) {
          if(newFilter) {
              $scope.ajax.loading = true;
              $http.get("/get/" + subtext + "/" + escape(newFilter)).
                  success(function(data) {
                    // Always expects, if any elements, a fields item in it
                    $scope.ajax.list = [];
                    data.forEach(function(e, i, l) {
                      $scope.ajax.list.push(e.fields);
                    });
                      $scope.ajax.loading = false;
                  }).
                  error(function() {
                      $scope.ajax.loading = false;
                  });
          }
          else {
              $scope.ajax.list = false;
          }
      },
      toModel: function(data, callback, subtext) {
          if(data) {
              callback(data.fields);
          }
          else {
              callback();
          }
      },
      toSelection: function(data, callback, subtext) {
          if(data) {
              $http.get("/get/" + subtext + "/" + escape(newFilter)).
                  success(function(response) {
                      callback(response.data.fields);
                  }).
                  error(function() {
                      callback();
                  });
          }
          else {
              callback();
          }
      },
      loading: false
  };

  $scope.cbSelect = {
    exec: function(type, newVal, oldVal) {
      $scope.formData[type] = newVal;
    }
  };

  $scope.submit = function() {
        $scope.ajax.loading = true;
        console.log("ELLO");
    };
})
