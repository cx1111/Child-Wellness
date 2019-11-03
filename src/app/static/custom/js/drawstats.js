// Draw the cumulative wordcount line graph

// alert(average_wordcount['0.1'][0].count);

// The parent div to draw the graph in
var parentDivName = "main-chart";
var parentDiv = document.getElementById(parentDivName);

// The tooltip function
var tip0 = d3
  .tip()
  .attr("class", "d3-tip")
  .offset([-10, 0])
  .html(function(d) {
    return d.wordcount;
  });

// Larger bottom margin to show x axis label
var margin = { top: 10, right: 50, bottom: 100, left: 80 },
  width = parentDiv.offsetWidth - margin.left - margin.right, // Use the window's width
  height = parentDiv.offsetWidth * 0.5 - margin.top - margin.bottom; // Use the window's height

// Data points from benchmarks
var datasetUpper = averageWordcount["0.75"];
var datasetLower = averageWordcount["0.25"];
// The number of datapoints
var n = datasetUpper.length;

// X scale will use the index of our data
var xScale = d3
  .scaleLinear()
  .domain([16, 31]) // xlim
  .range([0, width]); // output dom

// 6. Y scale will use the randomly generate number
var yScale = d3
  .scaleLinear()
  .domain([0, 650]) // ylim
  .range([height, 0]); // output

// 7. d3's line generator
var lineGenerator = d3
  .line()
  .x(function(d) {
    return xScale(d.age_months);
  }) // set the x values for the line generator
  .y(function(d) {
    return yScale(d.wordcount);
  }) // set the y values for the line generator
  .curve(d3.curveMonotoneX); // apply smoothing to the line

// 1. Add the SVG to the page and employ #2
var svg = d3
  .select("#" + parentDivName)
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Add the tooltips to the svg
svg.call(tip0);

// Call the x axis in a group tag
svg
  .append("g")
  .attr("class", "xaxis")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(xScale)); // Create an axis component with d3.axisBottom

// Call the y axis in a group tag
svg
  .append("g")
  .attr("class", "yaxis")
  .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft

// Append the path, bind the data, and call the line generator
svg
  .append("path")
  .datum(cumulativeWordcount)
  .attr("class", "line-child")
  .attr("d", lineGenerator);

svg
  .append("path")
  .datum(datasetUpper)
  .attr("class", "line-upper")
  .attr("d", lineGenerator);

svg
  .append("path")
  .datum(datasetLower)
  .attr("class", "line-lower")
  .attr("d", lineGenerator);

// Appends a circle for each datapoint
// With hover functionality
svg
  .selectAll(".dot")
  .data(cumulativeWordcount)
  .enter()
  .append("circle") // Uses the enter().append() method
  .attr("class", "dot-child") // Assign a class for styling
  .attr("cx", function(d) {
    return xScale(d.age_months);
  })
  .attr("cy", function(d) {
    return yScale(d.wordcount);
  })
  .attr("r", 5)
  .on("mouseover", function(d, i) {
    // make the mouseover'd element bigger
    d3.select(this)
      .transition()
      .duration(100)
      .attr("r", 15)
      .attr("fill", "#ff0000");
  })
  .on("mouseout", function(d, i) {
    // return the mouseover'd element
    d3.select(this)
      .transition()
      .duration(100)
      .attr("r", 5)
      .attr("fill", "#000000");
  })
  .on("click", function(d, i) {
    window.open("/videos/cleaning the basement 02-11-2019", "_blank");
  });

svg
  .selectAll(".dot")
  .data(datasetUpper)
  .enter()
  .append("circle")
  .attr("class", "dot-upper")
  .attr("cx", function(d) {
    return xScale(d.age_months);
  })
  .attr("cy", function(d) {
    return yScale(d.wordcount);
  })
  .attr("r", 5)
  .on("mouseover", tip0.show)
  .on("mouseout", tip0.hide);

svg
  .selectAll(".dot")
  .data(datasetLower)
  .enter()
  .append("circle")
  .attr("class", "dot-lower")
  .attr("cx", function(d) {
    return xScale(d.age_months);
  })
  .attr("cy", function(d) {
    return yScale(d.wordcount);
  })
  .attr("r", 5)
  .on("mouseover", tip0.show)
  .on("mouseout", tip0.hide);

// Add title if needed
// svg
//   .append("text")
//   .attr("class", "graph-title")
//   .attr("x", width / 2)
//   .attr("y", 0 - margin.top / 2)
//   .attr("text-anchor", "middle")
//   .text('Unique Words Expressed');

// Add axis labels
svg
  .append("text")
  .attr(
    "transform",
    "translate(" + width / 2 + " ," + (height + margin.bottom / 2) + ")"
  )
  .attr("class", "xlabel")
  .style("text-anchor", "middle")
  .text("Age in Months");

svg
  .append("text")
  .attr("transform", "rotate(-90)")
  .attr("y", 0 - margin.left)
  .attr("x", 0 - height / 2)
  .attr("dy", "1em")
  .attr("class", "ylabel")
  .style("text-anchor", "middle")
  .text("Unique Words Expressed");

// Add legend
svg
  .append("text")
  .attr("x", width * 0.95)
  .attr("y", 640 - cumulativeWordcount[cumulativeWordcount.length - 1].wordcount)
  .text(childName)
  .style("font-size", "20px")
  .attr("alignment-baseline", "middle");

svg
  .append("text")
  .attr("x", width * 0.95)
  .attr("y", 650 - datasetUpper[datasetUpper.length - 1].wordcount)
  .text("75th PCTL")
  .style("font-size", "20px")
  .attr("alignment-baseline", "middle");

svg
  .append("text")
  .attr("x", width * 0.95)
  .attr("y", 610 - datasetLower[datasetLower.length - 1].wordcount)
  .text("25th PCTL")
  .style("font-size", "20px")
  .attr("alignment-baseline", "middle");
