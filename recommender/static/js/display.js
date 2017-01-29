$("#user_loans").hide()

function sendData( input_id ) {
  var input_elem = $("#"+input_id);
  var username = input_elem.val()

  $.getJSON('/get_best_loans/'.concat(username), function (data) {
    console.log('in display function best loans')

    if(data) {
      $("#user_loans").show()

      // Plot elements of previous loans using high charts
      pie_chart(data[0]['user_countries'], 'Countries', 'countries_container')
      pie_chart(data[0]['user_continents'], 'Continents', 'continents_container')
      pie_chart(data[0]['user_sectors'], 'Sectors', 'sectors_container')
      pie_chart(data[0]['user_tags'], 'Tags', 'tags_container')
      pie_chart(data[0]['user_themes'], 'Themes', 'themes_container')

      tableCreate(data[1]);
    }
  });
}

function tableCreate( data ){
    tbl  = document.createElement('table');
    tbl.style.width  = '100%';
    tbl.style.border = '1px solid black';
    tbl.class = "table table-hover"

  //Create table header
  headers = ["", "Loan Similarity<sup><a href='#fn2' id='ref2'>2</a></sup>", "Name of Borrower",
             "Gender", "Country", "Continent", "Sector", "Description"]

  rows = {0: 'loan_link', 1: 'similarity', 2: 'borrower_name', 3: 'gender',
          4: 'country', 5: 'continent', 6: 'sector', 7: 'text'}

  function get_cell_value (i, j) {

    if(i == 0){
      return headers[j]
    }
    else if(j == 0){
      img_link = '<a href="'.concat(data[i-1]['loan_link']).concat('"><img src="').concat(data[i-1]['loan_img'])
      img_link = img_link.concat('" alt=').concat(data[i-1]['loan_id']).concat(' style="width:200px;">')
      return img_link
    }
    else {
      return data[i-1][rows[j]]
    }
  }

  console.log(data.length)
  for(var i = 0; i < data.length + 1; i++){
    var tr = tbl.insertRow();
    for(var j = 0; j < 8; j++){
      var td = tr.insertCell();
      td.appendChild(document.createTextNode(get_cell_value(i, j)));
      td.style.border = '1px solid black';
    }
  }
  $("#table_div").append(tbl);
}

