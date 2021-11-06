var getData

$( document ).ready(function() {
    plotly_canvas_result_table = document.getElementById('canvas-result-table')
    plotly_canvas_result_plot = document.getElementById('canvas-result-plot')

    getData = function (query_string) {
        query_string = $("#query-text-area").val();
        $.post( "/query", {
            query_string: query_string,
            test_val: 23
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

    $("#queryButton").click(function() {
        getData($("#query-text-area").val())
    })

    insertData = function (insert_string) {
      query_string = $("#insert-text-area").val();
      $.post( "/insert", {
          insert_string: insert_string
      },function(result, status){
          result_data = result['data']
      }, 'json')
    }

    $("#insertButton").click(function() {
      insertData($("#insert-text-area").val())
  })
})
