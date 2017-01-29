$("#user_loans").hide()


function sendData( input_id ) {
  var input_elem = $("#"+input_id);
  var username = input_elem.val()
  console.log(username)
    $.ajax({
       type:"GET",
        url: $SCRIPT_ROOT,
        data:username,
        success:function(data){
          console.log("success");
        },
        error:function(data){
          console.log("failure");
        }
    });
  $("#user_loans").show()

  $.getJSON('/get_best_loans/'.concat(username), function (data) {
    console.log('in display function best loans')

    // Plot elements of previous loans using high charts
    pie_chart(data[0]['user_countries'], 'Countries', 'countries_container')
    pie_chart(data[0]['user_continents'], 'Continents', 'continents_container')
    pie_chart(data[0]['user_sectors'], 'Sectors', 'sectors_container')
    pie_chart(data[0]['user_tags'], 'Tags', 'tags_container')
    pie_chart(data[0]['user_themes'], 'Themes', 'themes_container')

    console.log(data[1])
  });

}

