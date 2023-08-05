/*globals $, Morris, gettext*/
$(function () {
    $(".chart").css("height", "250px");
    new Morris.Area({
        element: 'obd_chart',
        data: JSON.parse($("#obd-data").html()),
        xkey: 'date',
        ykeys: ['ordered', 'paid'],
        labels: [gettext('Placed orders'), gettext('Paid orders')],
        lineColors: ['#000099', '#009900'],
        smooth: false,
        resize: true,
        fillOpacity: 0.3,
        behaveLikeLine: true
    });
    new Morris.Area({
        element: 'cbd_chart',
        data: JSON.parse($("#cbd-data").html()),
        xkey: 'date',
        ykeys: ['clicks'],
        labels: [gettext('Clicks')],
        lineColors: ['#990000'],
        smooth: false,
        resize: true,
        fillOpacity: 0.3,
        behaveLikeLine: true
    });
});
