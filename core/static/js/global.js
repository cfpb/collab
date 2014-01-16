$(document).ready(function() {

    $(".tag").tooltip({
        delay: 100
    });

    function showErrorOrRedirect(data) {
        if(data.redirect) {
            window.location.replace(data.redirect);
        } else {
            createAlert(data.error);
        }
    }

    function createAlert(msg) {
        $("#msg-bar-error").append("<div style='color: red;'>" + msg + "</div>");
    }

    window.submitOptions = { success: showErrorOrRedirect };
});
