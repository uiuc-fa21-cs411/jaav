var getData

$( document ).ready(function() {
    plotly_canvas_result_table = document.getElementById('canvas-result-table')
    plotly_canvas_result_plot = document.getElementById('canvas-result-plot')

    getData = function (query_string) {
        query_string = $("#sql-text-area").val();
        $.post( "/query", {
            query_string: query_string
        }, function(result, status){
            result_data = result['data']
        }, 'json')
    }

    $("#sendButton").click(function() {
        getData($("#sql-text-area").val())
    })
})
