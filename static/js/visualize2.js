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


function matrix(xdim, yearlabel, dataset)
{
    //    var margin = {top: 19.5, right: 19.5, bottom: 19.5, left: 39.5};
    var margin = {top: 0, right: 0, bottom: 0, left: 0};

    var width = 600 - margin.right, 
	iwidth = width / xdim[1],
	iheight = iwidth,
	height = iheight * xdim[0] - margin.top - margin.bottom,
	padding = 10;

    var colorScale = d3.scale.linear()
    	.domain([d3.min(dataset, function(d) {return d.data;}), 
		 d3.max(dataset, function(d) {return d.data;})])
    	.range([d3.rgb(255,0,0), d3.rgb(0,0,255)]);

    var title = d3.select("#chart").append("textlayer").append("div").append("text")
	    .attr("x", width/2)             
	    .attr("y", -height)
	    .attr("text-anchor", "middle")  
	    .style("font-size", "20px") 
	    .style("visibility", "visible")
	    .style("color", "#1f8dd6")
	    .text("Feature Space");

    var tooltip = d3.select("#chart")
	.append("div")
	.style("position", "absolute")
	.style("z-index", "10")
	.style("visibility", "hidden")
        .style("color", "red")
	.text("a simple tooltip");


    var grid = d3.select("#chart").append("chartlayer").append("svg")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom)
	.attr("class", "chart")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


	grid.append("rect")
	    .attr("width", "100%")
	    .attr("height", "100%")
	    .attr("fill", "#CCFFFF");


    var row = grid.selectAll(".row")
                  .data(dataset)
                .enter().append("svg:rect")
                 .attr("class", "cell")
                 .attr("x", function(d) { return d.j * iwidth; })
                 .attr("y", function(d) { return d.i * iheight; })
                 .attr("width", iwidth)
         	.attr("height", iheight)

	.text(function(d) { 
	    return tooltip.style("visibility", "visible")
	    .text(d.year);})

	.on("mouseover", function(d){
		return tooltip.style("visibility", "visible")
		.text(d.label);})
	.on("mousemove", function(){return tooltip.style("top",
							 (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");})
	//	.on("mouseout", function(){
	//		return tooltip.style("visibility", "hidden");})

	.style("fill", function(d) { return colorScale(d.data); });

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
