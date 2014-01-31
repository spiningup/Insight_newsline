function draw_wordcloud(width, height) {
      var fill = d3.scale.category20();
      d3.layout.cloud().size([width, height])
	  .words(["Alibaba", "Syria", "Obamacare", "gun control", "Facebook IPO", "Obama", "bitcoin", "government shutdown", "twitter", "data science", "apple China", "football concussions", "global warming", "smartphone", "climate conference", "financial crisis", "sochi winter", "snowden"].map(function(d) {
      return {text: d, size: 10 + Math.random() * 90};
      }))
      .padding(5)
      .rotate(0) // function() { return ~~(Math.random() * 2) * 90; })
      .font("Impact")
      .fontSize(function(d) { return d.size; })
      .on("end", draw)
      .start();

  function draw(words) {
    d3.select("#wordcloud").append("svg")
        .attr("width", width)
        .attr("height", height)
      .append("g")
        .attr("transform", "translate(" + width/2 + "," + height/2 + ")")
      .selectAll("text")
        .data(words)
      .enter().append("text")
        .style("font-size", function(d) { return d.size + "px"; })
        .style("font-family", "Impact")
        .style("fill", function(d, i) { return fill(i); })
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.text; })
	.on("click", function(d) 
	    { 
		window.open('/search?q='+d.text, '_self'); 
	    }); 

  }
}
