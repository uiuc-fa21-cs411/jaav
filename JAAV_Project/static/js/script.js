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
