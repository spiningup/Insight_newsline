function matrix(dataset)
{
    var width = 2;
    var height = 2;
    console.log(dataset);
    var grid = d3.select("#chart").append("svg")
                    .attr("width", width)
                    .attr("height", height)
                    .attr("class", "chart");

    var row = grid.selectAll(".row")
                  .data(calData)
                .enter().append("svg:g")
                  .attr("class", "row");

    var col = row.selectAll(".cell")
                 .data(function (d) { return d; })
                .enter().append("svg:rect")
                 .attr("class", "cell")
                 .attr("x", function(d) { return d.x; })
                 .attr("y", function(d) { return d.y; })
                 .attr("width", width)
                 .attr("height", height)
                 .on('mouseover', function() {
                    d3.select(this)
                        .style('fill', '#0F0');
                 })
                 .on('mouseout', function() {
                    d3.select(this)
                        .style('fill', '#FFF');
                 })
                 .on('click', function() {
                    console.log(d3.select(this));
                 })
                 .style("fill", '#FFF')
                 .style("stroke", '#555');
}


