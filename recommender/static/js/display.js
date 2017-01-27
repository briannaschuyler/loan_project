function updatePlots() {

  console.log('in display')
  $.getJSON('/countries_pie', function (data) {
    console.log('in display function  countries pie')
    console.log(data)
  })
  $.getJSON('/best_loans', function (data) {
      console.log('in display function  best loans`')
          console.log(data)
  })
pie_chart('/countries_pie', 'Countries');

}

window.onload = updatePlots();
