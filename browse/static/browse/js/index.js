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
    var review_id = $(this).closest('.card').attr('review-id');
    var action = $(this).attr('action');

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

