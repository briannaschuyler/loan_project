var pie_chart = function (data, title, container) {

    Highcharts.chart(container, {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: title
        },
       tooltip: {
            pointFormat: '{point.y} loans ({point.percentage:.1f} %)'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
            }
        },
        credits: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        series: [{
            data: data
        }]
       });
};
