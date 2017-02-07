$("#user_loans").hide();
$("#username_dne").hide();
$("#find_username").hide();

function findUsername() {
  $("#username_dne").hide();
  $("#find_username").show();
  $("#user_loans").hide();

}

function validateGood( loan_id ) {
  $('#bad_'.concat(loan_id)).hide();
  $('#why_'.concat(loan_id)).show();
  $('#submit_'.concat(loan_id)).show();
}

function validateBad( loan_id ) {
  $('#good_'.concat(loan_id)).hide();
  $('#why_'.concat(loan_id)).show();
  $('#submit_'.concat(loan_id)).show();
}
function submitValidation( loan_id ) {
  $('#why_'.concat(loan_id)).hide();
  $('#submit_'.concat(loan_id)).hide();
  $('#thanks_'.concat(loan_id)).show();
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

  if ($('#loan_table').length > 0) {
    // If the table already exists, remove the rows and create new ones specific to the most
    // recent query.
    $("#loan_table tr").remove();
  }

  //Create new table with details on best fit loans
  tbl  = document.createElement('table');
  tbl.id = 'loan_table'
  tbl.style.width  = '100%';
  tbl.style.border = '1px solid black';
  tbl.class = "table table-hover";

  //Create table header
  headers = [" ", "Loan Similarity<sup><a href='#fn2' id='ref2'>2</a></sup>", "Name of Borrower",
             "Gender", "Country", "Continent", "Sector", "Tags",  "Themes", "Description", "Validation Measure"]

  rows = {0: 'loan_link', 1: 'similarity', 2: 'borrower_name', 3: 'gender',
          4: 'country', 5: 'continent', 6: 'sector', 7: 'tags', 8: 'themes', 9: 'text'}

  function get_cell_value (i, j) {

    if (i > 0) {
      var loan_id = data[i-1]['loan_id']
    }
    if(i == 0){
      return '<h6>'.concat(headers[j]).concat('</h6>')
    }
    else if(j == 0){
      img_link = '<a href="'.concat(data[i-1]['loan_link']).concat('"><img src="');
      img_link = img_link.concat(data[i-1]['loan_img']).concat('" alt=');
      img_link = img_link.concat(loan_id).concat(' style="width:200px;">');
      return img_link
    }
    else if(j == 9) {
      var description = ['<a href="#" data-toggle="tooltip" title="',
                         data[i-1]['text'], '">Hover<br>For<br>Full<br>Description</a>'].join('');
      return description
    }
    else if(j == 10) {
      // Make Good/Bad loan validation buttons and text for explanation.  These results don't
      // actually get saved anywhere right now, they're more of a proof of concept.
      var goodFit = ['<button type="button" class="btn btn-xs btn-success" id="good_', loan_id,
                     '" onclick="validateGood(', loan_id, ')">Good Fit</button>'].join('');

      var badFit = ['<button type="button" class="btn btn-xs btn-danger" id="bad_', loan_id,
                    '" onclick="validateBad(', loan_id, ')">Poor Fit</button>'].join('');

      var expl = ['</div><input type="text" name="validation" size="7" id="why_', loan_id,
                  '" value="Why?">'].join('');

      var submitExpl = ['<button type="button" class="btn btn-xs btn-default" id="submit_', loan_id,
                        '" onclick="submitValidation(', loan_id, ')">Submit</button>'].join('');

      var thanks = ['<div id="thanks_', loan_id, '">Thanks!</div>'].join('');

      return ['<div class="btn-group-vertical">', goodFit, badFit, expl, submitExpl, thanks].join('\n')
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
      td.style.textAlign = 'center';
      if(i == 0){
        td.style.backgroundColor = 'black';
        td.style.color = 'white';
      }
    }
  }
  $("#loan_table_div").append(tbl);

  // Hide all of the "Why?" text in the validation measure
  for (var i = 0; i < data.length; i++){
    $("#why_".concat(data[i]['loan_id'])).hide()
    $("#submit_".concat(data[i]['loan_id'])).hide()
    $("#thanks_".concat(data[i]['loan_id'])).hide()
  }
}

function notImplemented(){
  alert("Ok, this function isn't currently implemented.  But it would be pretty cool, right?!");
}
