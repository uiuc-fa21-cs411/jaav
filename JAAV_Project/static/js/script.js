var getData
var getFavoriteTrails

$( document ).ready(function() {
    plotly_canvas_result_table = document.getElementById('canvas-result-table')
    plotly_canvas_result_plot = document.getElementById('canvas-result-plot')
    q1_result = document.getElementById('q1')
    q2_result = document.getElementById('q2')

    getData = function (query_string, select_query_1, select_query_2, update_fav_trail_usrnm, update_fav_trail_trlnm) {
        console.log("call getData")
        query_string = $("#sql-text-area").val();
        create_user = document.getElementById("create-user").value;
        create_pass = document.getElementById("create-pass").value;
        select_query_1 = 0;
        select_query_2 = 0;
        del_user = 0;
        latitude = document.getElementById("sql-procedure-latitude").value;
        longitude = document.getElementById("sql-procedure-longitude").value;
        distance = document.getElementById("sql-procedure-size").value;
        
        if (document.getElementById("delete-user").checked) {
          del_user = 1;
        }
        if (q1_result.checked) {
            select_query_1 = 1;
        }
        if (q2_result.checked) {
            select_query_2 = 1;
        }

        $.post( "/info/query", {
            query_string: query_string,
            select_query_1: select_query_1,
            select_query_2: select_query_2,
            del_user: del_user,
            create_user: create_user,
            create_pass: create_pass,
            longitude : longitude,
            latitude : latitude,
            distance : distance
        }, function(result, status){
            result_data = result['data']

            var data = [{
                type: 'table',
                header: {
                  values: result_data['labels'],
                  align: "center",
                  line: {width: 1, color: 'black'},
                  fill: {color: "grey"},
                  font: {family: "Arial", size: 12, color: "white"}
                },
                cells: {
                  values: result_data['values'],
                  align: "center",
                  line: {color: "black", width: 1},
                  font: {family: "Arial", size: 11, color: ["black"]}
                }
            }]
            Plotly.newPlot(plotly_canvas_result_table, data);

            // update bar chart
            // var bar_data = [
            //     {
            //         type: 'bar',
            //         x: result_data['values'][0],
            //         y: result_data['values'][1]
            //     }
            // ]
            // Plotly.newPlot(plotly_canvas_result_plot, bar_data)
        }, 'json')
    }

    getFavoriteTrails = function (update_fav_trail_usrnm, update_fav_trail_trlnm) {
      console.log("call getFavoriteTrails")
      update_fav_trail_usrnm = document.getElementById('ft-updateFavTrail-username').value;
      update_fav_trail_trlnm = document.getElementById('ft-updateFavTrail-trail').value;
      add_trail_user = document.getElementById("ft-add-trail-user").value;
      add_trail_name = document.getElementById("ft-add-trail-name").value;
      del_trail = 0;
      if (document.getElementById("delete-trail").checked) {
        del_trail = 1;
      }
      $.post( "/ftrails/query", {
          update_fav_trail_usrnm: update_fav_trail_usrnm,
          update_fav_trail_trlnm: update_fav_trail_trlnm,
          add_trail_user: add_trail_user,
          add_trail_name: add_trail_name,
          del_trail: del_trail
      }, function(result, status){
          result_data = result['data']
          console.log(result_data)
          var data = [{
              type: 'table',
              header: {
                values: result_data['labels'],
                align: "center",
                line: {width: 1, color: 'black'},
                fill: {color: "grey"},
                font: {family: "Arial", size: 12, color: "white"}
              },
              cells: {
                values: result_data['values'],
                align: "center",
                line: {color: "black", width: 1},
                font: {family: "Arial", size: 11, color: ["black"]}
              }
          }]
          Plotly.newPlot(plotly_canvas_result_table, data);
      }, 'json')
    }

    $("#sendButton").click(function() {
        console.log("hi")
        getData($("#sql-text-area").val(), $("#q1").val(), $("#q2").val(), $("#sql-updateFavTrail-username").val(), $("#sql-updateFavTrail-trail").val())
    });

    $("#FavTrailsButton").click(function() {
      console.log("HEY")
      getFavoriteTrails($("#ft-updateFavTrail-username").val(), $("#ft-updateFavTrail-trail").val())
    })
    
})