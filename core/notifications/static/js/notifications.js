function notifications_ready() {
    $('.notification-counter').click(function() {
        $(this).toggleClass('active');
        $('#notifications-widget').fadeToggle(100);
    });
    $('.notification').each(function() {
        var notification = $(this);
        notification.find('.hide').first().click(function() {
            hide_notification(notification);
            return false;
        })
        $(this).click(function() {
            hide_notification(notification);
            return true;
        })
    })
    $('.hide-all').click(function() {
        hide_all_notifications($('.notification'))
        return true;
    })
}

function hide_notification(element) {
    $.post('/notifications/mark_as_read/' + element.attr('data-id'), function() {
        element.remove();
        update_notification_counter()
    })
}

function hide_all_notifications(elements) {
  elements.each(function() {
    $(this).remove();
  })
  $.post('/notifications/mark_all_as_read/', function() {
    update_notification_counter()
  })
}

function update_notification_counter() {
    var total = $('.notifications .notification').length
    if (total < 2) {
        $('.hide-all').hide();
    }
    if (total > 0) {
        $('.notification-counter span').html(total);
    } else {
        $('.notifications').hide();
        $('.notification-counter').fadeOut(100);
    }


}
