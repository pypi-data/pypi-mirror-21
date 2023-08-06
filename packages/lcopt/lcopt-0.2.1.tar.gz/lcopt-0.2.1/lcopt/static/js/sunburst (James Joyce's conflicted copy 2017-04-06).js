 $(document).ready(function(){ var width = 960,
        height = 700,
        radius = (Math.min(width, height) / 2) - 10;
  
    var formatNumber = d3.format(",f");
  
    var x = d3.scaleLinear()
        .range([0, 2 * Math.PI]);
  
    var y = d3.scaleSqrt()
        .range([0, radius]);
  
    var color = d3.scaleOrdinal(d3.schemeCategory20);
  
    var partition = d3.partition();
  
    var arc = d3.arc()
        .startAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x0))); })
        .endAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x1))); })
        .innerRadius(function(d) { return Math.max(0, y(d.y0)); })
        .outerRadius(function(d) { return Math.max(0, y(d.y1)); });
  
  
    //var svg = d3.select("body").append("svg")
    var svg = d3.select("#sunburst")
        .attr("width", width)
        .attr("height", height)
      .append("g")
        .attr("transform", "translate(" + width / 2 + "," + (height / 2) + ")");
  
    d3.json("/results.json", function(error, root) {
      if (error) throw error;
      
      root = d3.hierarchy(root.results[2][0].graph, function(d){return d.technosphere});
      console.log(root)
      console.log(partition(root))
      root.sum(function(d) { if (d.biosphere[0]){bio_impact = d.biosphere[0].impact}else{bio_impact=0}; return d.impact + bio_impact; });
      svg.selectAll("path")
          .data(partition(root).descendants())
        .enter().append("path")
          .attr("d", arc)
          .style("fill", function(d) { return color(d.data.activity); })//return color((d.children ? d : d.parent).data.activity); })
          .on("click", click)
        .append("title")
          .text(function(d) { console.log(d.data.activity + "\n" + formatNumber(d.value)); return d.data.activity + "\n" + formatNumber(d.value); });
    });
  
    function click(d) {
      svg.transition()
          .duration(750)
          .tween("scale", function() {
            var xd = d3.interpolate(x.domain(), [d.x0, d.x1]),
                yd = d3.interpolate(y.domain(), [d.y0, 1]),
                yr = d3.interpolate(y.range(), [d.y0 ? 20 : 0, radius]);
            return function(t) { x.domain(xd(t)); y.domain(yd(t)).range(yr(t)); };
          })
        .selectAll("path")
          .attrTween("d", function(d) { return function() { return arc(d); }; });
    }
  
    d3.select(self.frameElement).style("height", height + "px");})