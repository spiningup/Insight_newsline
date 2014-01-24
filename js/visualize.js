function queryURL(query) {
    $("#query").val(query);
    visualize();	
}

function visualize() {
    var url = "/analyze";
    var Q = $("#query").val();

    var html = '<img src="static/img/ajaxSpinner.gif" alt="Please wait" width=30px height=30px>';
    $("#spinner").html(html);    
    $( "#google-table" ).empty();
    $.post(url, {'jobQuery':Q}, cback); 

}

function visualize_features() {
    var url = "/topics";
    var Q = $("#query").val();

    var html = '<img src="static/img/ajaxSpinner.gif" alt="Please wait" width=30px height=30px>';
    $("#spinner").html(html);
    $(".timeline-jquery").empty();
    $.post(url, {'jobQuery':Q}, cback_features); 

}


function drawChart(results) {
  var container = document.getElementById('google-table');
  var googlechart = new google.visualization.Timeline(container);
  var dataTable = new google.visualization.DataTable();
  var d = results['topics'];

  dataTable.addColumn({ type: 'string', id: 'No. Topic' });
  dataTable.addColumn({ type: 'string', id: 'Topic' });
  dataTable.addColumn({ type: 'date', id: 'Start' });
  dataTable.addColumn({ type: 'date', id: 'End' });

  for (var i=0; i <= d.length-1; i++) {
  dataTable.addRows([
    [(i+1).toString(), d[i].term, new Date(d[i].syear, d[i].smonth, d[i].sday), 
     new Date(d[i].eyear, d[i].emonth, d[i].eday)]]);
  }

  var options = {
    colors: ['#0BB4C4', '#0BB4C4', '#26CEDD', '#26CEDD', '#24E2D9', '#24E2D9', '#12EDD7', '#12EDD7', '#09F9E5', '#09F9E5'],
    timeline: { rowLabelStyle: {fontName: 'Lucida Console', fontSize: 18, color: '#603913' },
                barLabelStyle: { fontName: 'Lucida Console', fontSize: 18 }, 
              }, 

  };

  googlechart.draw(dataTable, options);

  d3.select("#google-table").selectAll("svg text").attr("font-size", 18).attr("font-family", 'Lucida Console');

}

function cback(results) {
    window.history.pushState("", "Newsline", "/search?q="+results['query']);

    //    $("chartlayer").remove();
    //    $("textlayer").remove();
    $("#spinner").html('');
    $("#summarybut").css("background", "#fff");
    $("#summarybut").css("color", "#666");
    $("#summarybut").css("border", "1px solid #ddd");
    $("#timelinebut").css("background", "#02a6eb");
    $("#timelinebut").css("color", "#fff");
    $("#timelinebut").css("border", "0px");

    $('.timeline-jquery').verticalTimeline({
       data: results['items'],
       width: '100%',
      });

}


function cback_features(results) {
    //    matrix(results['dim'], results['yearlabel'], results['X']);
    //    $("#chart").show();

    //    $("#hottopics").html("<font size=6>Top 10 Topics </font>");
    //   $( "#hottopics" ).hide();

    $("#spinner").html('');
    $("#timelinebut").css("background", "#fff");
    $("#timelinebut").css("color", "#666");
    $("#timelinebut").css("border", "1px solid #ddd");
    $("#summarybut").css("background", "#02a6eb");
    $("#summarybut").css("color", "#fff");
    $("#summarybut").css("border", "0px");

    $("#google-table").css("width", "650px");
    $("#google-table").css("height", "700px");
    $("#google-table").css("margin-top", "40px");
    drawChart(results);

}
