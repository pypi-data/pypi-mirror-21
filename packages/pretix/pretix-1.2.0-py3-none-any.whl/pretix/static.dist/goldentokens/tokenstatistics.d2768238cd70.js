/*globals $, Morris, gettext*/
$(function () {
    $(".chart").css("height", "250px");
    new Morris.Area({
        element: 'vpd_chart',
        data: JSON.parse($("#vpd-data").html()),
        xkey: 'date',
        ykeys: ['amount'],
        labels: [gettext('Replicated vouchers')],
        smooth: false,
        resize: true,
        fillOpacity: 0.3,
        behaveLikeLine: true
    });
});
