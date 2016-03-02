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

    var review_div = $(this).closest('.card');
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
      url: "new/add_vote",
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
