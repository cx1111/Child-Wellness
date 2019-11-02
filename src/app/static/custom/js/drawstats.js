// Draw the cumulative wordcount line graph

// alert(average_wordcount['0.1'][0].count);

// The parent div to draw the graph in
var parentDivName = "main-chart";
var parentDiv = document.getElementById(parentDivName);

var margin = { top: 50, right: 50, bottom: 50, left: 50 },
  width = parentDiv.offsetWidth - margin.left - margin.right, // Use the window's width
  height = parentDiv.offsetWidth * 0.66 - margin.top - margin.bottom; // Use the window's height

// Data points from benchmarks
var datasetUpper = averageWordcount["0.9"];
var datasetLower = averageWordcount["0.1"];
// The number of datapoints
var n = datasetUpper.length;

// 5. X scale will use the index of our data
var xScale = d3
  .scaleLinear()
  .domain([16, 31]) // xlim
  .range([0, width]); // output dom

// 6. Y scale will use the randomly generate number
var yScale = d3
  .scaleLinear()
  .domain([0, 700]) // ylim
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

// 3. Call the x axis in a group tag
svg
  .append("g")
  .attr("class", "x axis")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(xScale)); // Create an axis component with d3.axisBottom

// 4. Call the y axis in a group tag
svg
  .append("g")
  .attr("class", "y axis")
  .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft

// 9. Append the path, bind the data, and call the line generator
// svg
//   .append("path")
//   .datum(dataset) // 10. Binds data to the line
//   .attr("class", "line") // Assign a class for styling
//   .attr("d", line); // 11. Calls the line generator

svg
  .append("path")
  .datum(cumulativeWordcount)
  .attr("class", "line")
  .attr("d", lineGenerator);

svg
  .append("path")
  .datum(datasetUpper)
  .attr("class", "line-upper")
  .attr("d", lineGenerator);

svg
  .append("path")
  .datum(datasetLower)
  .attr("class", "line-upper")
  .attr("d", lineGenerator);

// 12. Appends a circle for each datapoint

svg
  .selectAll(".dot")
  .data(cumulativeWordcount)
  .enter()
  .append("circle") // Uses the enter().append() method
  .attr("class", "dot") // Assign a class for styling
  .attr("cx", function(d) {
    return xScale(d.age_months);
  })
  .attr("cy", function(d) {
    return yScale(d.wordcount);
  })
  .attr("r", 5);

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
  .attr("r", 5);

svg
  .selectAll(".dot")
  .data(datasetLower)
  .enter()
  .append("circle")
  .attr("class", "dot-upper")
  .attr("cx", function(d) {
    return xScale(d.age_months);
  })
  .attr("cy", function(d) {
    return yScale(d.wordcount);
  })
  .attr("r", 5);
