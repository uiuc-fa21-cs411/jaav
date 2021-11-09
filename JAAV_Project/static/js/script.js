var getData

$( document ).ready(function() {
    plotly_canvas_result_table = document.getElementById('canvas-result-table')
    plotly_canvas_result_plot = document.getElementById('canvas-result-plot')
    q1_result = document.getElementById('q1')
    q2_result = document.getElementById('q2')

    getData = function (query_string, select_query_1, select_query_2, update_fav_trail_usrnm, update_fav_trail_trlnm) {
        query_string = $("#sql-text-area").val();
        update_fav_trail_usrnm = document.getElementById('sql-updateFavTrail-username').value;
        update_fav_trail_trlnm = document.getElementById('sql-updateFavTrail-trail').value;
        custom_query = document.getElementById('sql-query-input').value;
        create_user = document.getElementById("create-user").value;
        create_pass = document.getElementById("create-pass").value;
        add_trail_user = document.getElementById("add-trail-user").value;
        add_trail_name = document.getElementById("add-trail-name").value;
        select_query_1 = 0;
        select_query_2 = 0;
        del_user = 0;
        del_trail = 0;
        
        if (document.getElementById("delete-user").checked) {
          del_user = 1;
        }
        if (document.getElementById("delete-trail").checked) {
          del_trail = 1;
        }
        if (q1_result.checked) {
            select_query_1 = 1;
        }
        if (q2_result.checked) {
            select_query_2 = 1;
        }

        $.post( "/query", {
            query_string: query_string,
            select_query_1: select_query_1,
            select_query_2: select_query_2,
            update_fav_trail_usrnm: update_fav_trail_usrnm,
            update_fav_trail_trlnm: update_fav_trail_trlnm,
            custom_query: custom_query,
            del_trail: del_trail,
            del_user: del_user,
            create_user: create_user,
            create_pass: create_pass,
            add_trail_user: add_trail_user,
            add_trail_name: add_trail_name
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

            Plotly.newPlot(plotly_canvas_result_table, data)

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

    $("#sendButton").click(function() {
        getData($("#sql-text-area").val(), $("#q1").val(), $("#q2").val(), $("#sql-updateFavTrail-username").val(), $("#sql-updateFavTrail-trail").val())
    })
})