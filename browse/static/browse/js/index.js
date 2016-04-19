var primary_color = "blue";

// This just toggles the follow/following of the button
$('a.follow').click(function () {
  $(this).toggleClass('followed');
  
  if($(this).hasClass('followed')) {
    $(this).text('Followed');
    $('ul li:last-child').html('325<span>Followers</span>');
  }
  else {
    $(this).text('Follow Nick');
    $('ul li:last-child').html('324<span>Followers</span>');
  }
});


$(document).ready(function() {
  $('button').click(function() {
    var action = $(this).attr('action');

    var review_div = $(this).closest('.review-card-small,.card');
    var review_id = review_div.attr('review-id');

    var up = $(review_div).find("button.vote-button-up");
    var down = $(review_div).find("button.vote-button-down");

    if (action == "up") {
      var toggler = up;
      var remover = down;
    }
    else if (action == "down") {
      var toggler = down;
      var remover = up;
    }
    else {
      return;
    }

    if (remover) {
      $(remover).removeClass("vote-button-active");
    }
    if (toggler) {
      $(toggler).toggleClass("vote-button-active");
    }

    $.ajax({
      url: "/new/add_vote",
      type: "POST",
      data: {
        "review-id": review_id,
        "action": action
      }
    });
  });
});


// Hacky, but we have to have btn--color for all vote buttons as ripple uses it.
$(document).ready(function() {
  $('.vote-button-up,.vote-button-down').each(function() {
    $(this).addClass("btn--" + primary_color);
  });
});

/* Sidebar */
app.controller('leftCtrl', function ($scope, $timeout, $mdSidenav, $log) {
    $scope.toggle = buildToggler('left');
    /**
     * Supplies a function that will continue to operate until the
     * time is up.
     */
    function debounce(func, wait, context) {
      var timer;
      return function debounced() {
        var context = $scope,
            args = Array.prototype.slice.call(arguments);
        $timeout.cancel(timer);
        timer = $timeout(function() {
          timer = undefined;
          func.apply(context, args);
        }, wait || 10);
      };
    }
    /**
     * Build handler to open/close a SideNav; when animation finishes
     * report completion in console
     */
    function buildDelayedToggler(navID) {
      return debounce(function() {
        $mdSidenav(navID)
          .toggle()
          .then(function () {
            $log.debug("toggle " + navID + " is done");
          });
      }, 200);
    }
    function buildToggler(navID) {
      return function() {
        $mdSidenav(navID)
          .toggle()
          .then(function () {
            $log.debug("toggle " + navID + " is done");
          });
      }
    }
  })
