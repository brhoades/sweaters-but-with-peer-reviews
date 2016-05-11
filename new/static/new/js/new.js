$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
  }
);

app.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('blue', {
      'default': '500'
    })
    .accentPalette('orange', {
      'default': 'A200'
    });
});

// Expects a model param
app.controller('form-handler',
    function($scope, $http, $window, $attrs, LxDialogService, LxNotificationService) {
  $scope.type = $attrs.model;
  $scope.edit = $attrs.edit;
  $scope.report_model = $attrs.reportmodel;
  $scope.report_id = $attrs.reportid;

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

  // Get our field names automatically
  $http.get("/get/get_fields_for_model/" + $scope.type).success(function(data) {
    data.forEach(function(e, i, l) {
      $scope.data[e] = "";
      $scope.valid[e] = "";
      $scope.original[e] = "";
    });

    // review sliders
    if($scope.type == "review") {
      $scope.data.rating_overall = 2.5;
      $scope.data.rating_value = 2.5;
      $scope.data.rating_difficulty = 2.5;
    }

    // FIXME make this an option for ^
    if($scope.edit) {
      // grab the data
      $http.get("/get/model_values/" + $scope.type + "/" + $scope.edit + "/").success(function(form_data) {
        // Pop it into our form, with only the necessary values
        data.forEach(function(e, i, l) {
          $scope.data[e] = form_data[e];
        });
        $scope.id = form_data["id"];
      });
    }
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
                    if(e.fields != undefined && e.fields.id == undefined) {
                      e.fields["id"] = e.pk;  // move this over for later
                      $scope.ajax.list.push(e.fields);
                    }
                    else {
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
    var url = "/new/" + $scope.type;
    if($scope.edit) {
      url = "/edit/" + $scope.type + "/" + $scope.id;
    }
    if($scope.type == "report") {
      url = "/new/report/" + $scope.report_model + "/" + $scope.report_id;
    }
    if($scope.type == "resolve_report") {
      url = "/new/resolve_report/" + $scope.report_id;
    }

    $http.post(url, JSON.stringify($scope.data)).
      success(function(data) {
        // Always expects, if any elements, a fields item in it
        $scope.ajax.list = [];
        $scope.ajax.loading = false;
        $scope.valid = angular.copy($scope.original);

        if(data != undefined && data.error != undefined) {
          if(data.error.error) {
            // There's an overall error.
            LxNotificationService.error(data.error.error);
          }
          else {
            $scope.valid = data.error;
          }
        }
        if(data != undefined && data.id != undefined) {
          var redirectPage = "";
          var redirectID = "";
          if($scope.type == "reviewcomment") {
            redirectPage = "review";
            redirectID = $scope.data.target;
          }
          else {
            redirectPage = $scope.type;
            redirectID = data.id;
          }

          $http.get("/get/view_for_model_at_id/" + redirectPage + "/" + redirectID).
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
}]).directive('chooseFile', function() {
    return {
      link: function ($scope, elem, attrs) {
        var button = elem.find('button');
        var input = angular.element(elem[0].querySelector('input#fileInput'));

        button.bind('click', function() {
          input[0].click();
        });

        input.bind('change', function(e) {
          $scope.$apply(function() {
            var image;
            console.log(e);
            var files = e.target.files;
            if (files[0]) {
              $scope.fileName = files[0].name;
              image = files[0];
            } else {
              $scope.fileName = image;
            }

            if (image) {
              var reader = new FileReader();
              $scope.data.avatar = reader.readAsDataURL(image);
            }
          });
        });
      }
    };
  });
