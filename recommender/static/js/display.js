$("#user_loans").hide()
$("#username_dne").hide()
$("#find_username").hide()

function findUsername() {
  $("#username_dne").hide()
  $("#find_username").show()
  $("#user_loans").hide()

}

function sendData( input_id ) {
  var input_elem = $("#"+input_id);
  var username = input_elem.val()
  if(username == null || username == '') {
    $("#find_username").show();
  }
  else {
    $.getJSON('/get_best_loans/'.concat(username), function (data) {

      if(data.length == 0) {
        // If username does not exist or there's an error pinging the API, display instructions
        // // for how to access username
        $("#username_dne").show()
        $("#find_username").show()
      }
      else {
        $("#username_dne").hide()
        $("#find_username").hide()
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
}

function tableCreate( data ){
  tbl  = document.createElement('table');
  tbl.style.width  = '100%';
  tbl.style.border = '1px solid black';
  tbl.class = "table table-hover"

  //Create table header
  headers = [" ", "Loan Similarity<sup><a href='#fn2' id='ref2'>2</a></sup>", "Name of Borrower",
             "Gender", "Country", "Continent", "Sector", "Description", "Validation Measure"]

  rows = {0: 'loan_link', 1: 'similarity', 2: 'borrower_name', 3: 'gender',
          4: 'country', 5: 'continent', 6: 'sector', 7: 'text'}

  function get_cell_value (i, j) {

    if(i == 0){
      return '<h6>'.concat(headers[j]).concat('</h6>')
    }
    else if(j == 0){
      img_link = '<a href="'.concat(data[i-1]['loan_link']).concat('"><img src="');
      img_link = img_link.concat(data[i-1]['loan_img']).concat('" alt=');
      img_link = img_link.concat(data[i-1]['loan_id']).concat(' style="width:200px;">');
      return img_link
    }
    else if(j == 8) {
      validation =  '<div class="btn-group-vertical">'
      validation = validation.concat('<button type="button" class="btn btn-xs btn-success">Good Fit</button>');
      validation = validation.concat('<button type="button" class="btn btn-xs btn-danger">Poor Fit</button>');
      validation = validation.concat('</div><input type="text" name="validation" size="7" value="Why?">');
      return validation
    }
    else {
      return data[i-1][rows[j]]
    }
  }

  for(var i = 0; i < data.length + 1; i++){
    var tr = tbl.insertRow();
    for(var j = 0; j < headers.length; j++){
      var td = tr.insertCell();
      td.innerHTML = get_cell_value(i, j);
      td.style.border = '1px solid black';
      if(i == 0){
        td.style.fill = 'black';
      }
    }
  }
  $("#loan_table").append(tbl);
}

