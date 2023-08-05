/*global $ */

$(function () {
    // Cookie
    var cookie_name = $("#cookie_close").attr("data-cookie-name");
    $("#cookie_close").click(function (e) {
        document.cookie = cookie_name + "=yes; expires=Tue, 01 Jan 2037 12:00:00 UTC; path=/";
        $("#cookie").slideUp();
        e.preventDefault();
        return true;
    });
    if (document.cookie.search(cookie_name) >= 0) {
        $("#cookie").remove();
    }
    if ($("#cookie").length > 0) {
        $("body").css("padding-bottom", $("#cookie").height());
    }
});
