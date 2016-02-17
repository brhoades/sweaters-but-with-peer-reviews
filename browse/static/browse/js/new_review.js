$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
  }
);

angular.module('lumxWrap').controller('getReviewForm', function($scope, $http, $window) {
  $scope.data = {
    error: ""
  };

  $scope.valid = {
    error: "",
  };

  // Get our field names automatically
  $http.get("/get/get_fields_for_model/review").success(function(data) {
    data.forEach(function(e, i, l) {
      $scope.data[e] = "";
      $scope.valid[e] = "";
    });
  });

  $scope.description = {
    update: function(newVal) {
      $scope.formData["text"] = newVal;
    }
  };

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
                      e.fields["id"] = e.pk;  // move this over for later
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
      loading: false
  };

  $scope.cbSelect = {
    exec: function(type, newVal) {
      // $scope.data[type] = newVal;
      // console.log($scope.formData);
    }
  };

  $scope.submit = function() {
    $scope.ajax.loading = true;
    $http.post("/new/review", JSON.stringify($scope.data)).
      success(function(data) {
        // Always expects, if any elements, a fields item in it
        $scope.ajax.list = [];
        $scope.ajax.loading = false;
        $scope.valid = {
          error: "",
          text: "",
          target: "",
          course: ""
        };
        if(data != undefined && data.error != undefined) {
          $scope.valid = data.error;
        }
        if(data.redirect != undefined) {
          $window.location.href = data.redirect;
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
