var pie_chart = function (flask_path, title) {

    $.getJSON(flask_path, function (data) {

    console.log('inside here too');
    console.log(data);
    Highcharts.chart('countries_container', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: data[1]
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
        series: [{
            data: data[0]
        }]
       });
    });
};
