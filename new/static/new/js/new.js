$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
  }
);

var app = angular.module('lumxWrap', ['lumx', 'ngMaterial']);

app.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('blue', {
      'default': '500'
    })
    .accentPalette('pink', {
      'default': 'A200'
    });
});

// Expects a model param
app.controller('form-handler',
    function($scope, $http, $window, $attrs, LxDialogService) {
  $scope.type = $attrs.model;

  $scope.data = {
    error: ""
  };

  $scope.valid = {
    error: "",
  };

  $scope.original = {
    error: "",
  };

  $scope.opendDialog = function(dialogId) {
    LxDialogService.open(dialogId);
  };

  $scope.closingDialog = function() {
  };

  // school slider
  $scope.data.rating_overall = 2.5;
  $scope.data.rating_value = 2.5;
  $scope.data.rating_difficulty = 2.5;

  // Get our field names automatically
  $http.get("/get/get_fields_for_model/" + $scope.type).success(function(data) {
    data.forEach(function(e, i, l) {
      $scope.data[e] = "";
      $scope.valid[e] = "";
      $scope.original[e] = "";
    });
  });

  $scope.ajax = {
      list: [],
      update: function(newFilter, oldFilter, subtext) {
          if(newFilter) {
              $scope.ajax.loading = true;
              $http.get("/get/" + subtext + "/" + escape(newFilter)).
                  success(function(data) {
                    // Always expects, if any elements, a fields item in it
                    $scope.ajax.list = [];
                    data.forEach(function(e, i, l) {
                      if(e.fields != undefined && e.fields.id == undefined)
                      {
                        e.fields["id"] = e.pk;  // move this over for later
                        $scope.ajax.list.push(e.fields);
                      }
                      else
                      {
                        $scope.ajax.list.push(e);
                      }
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
      loading: false
  };

  $scope.submit = function() {
    $scope.ajax.loading = true;
    $http.post("/new/" + $scope.type, JSON.stringify($scope.data)).
      success(function(data) {
        console.log(data);
        // Always expects, if any elements, a fields item in it
        $scope.ajax.list = [];
        $scope.ajax.loading = false;
        $scope.valid = angular.copy($scope.original);

        if(data != undefined && data.error != undefined) {
          $scope.valid = data.error;
        }
        if(data != undefined && data.id != undefined) {
          $http.get("/get/view_for_model_at_id/" + $scope.type + "/" + data.id).
              success(function(data) {
                // Always expects, if any elements, a fields item in it
                  $window.location.href = data.url;
              }).
              error(function() {
                  $scope.ajax.loading = false;
              });
        }
      }).
    error(function() {
      $scope.ajax.loading = false;
    });
  };
}).config(['$httpProvider', function($httpProvider) {
  // send tokens
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

