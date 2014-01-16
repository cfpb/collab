function drawBarChart(data) {

    function getname(d) { return d.name; }
    function getval(d) { return d.value; }

    var width = 1220,
        height = 18 * data.length;
    var chart = d3.select("#users_by_division_viz")
                    .append("svg")
                        .attr("class", "chart")
                        .attr("width", width + 30)
                        .attr("height", height + 30)
                    .append("g")
                        .attr("transform", "translate(250, 25)");

    var x = d3.scale.linear()
                .domain([0, 500])
                .range([0, width/2]);

    var y = function(i) { return i * (height / data.length); };

    chart.selectAll("rect")
            .data(data.map(getval))
         .enter()
            .append("rect")
                .attr("y", function(d, i) { return y(i); })
                .attr("width", 0)
                .attr("height", 16);

    chart.selectAll("text.inbar")
            .data(data)
         .enter()
            .append("text")
                .attr("x", function(d, i) { return x(getval(d));})
                .attr("y", function(d, i) { return y(i); })
                .attr("dx", -3) // padding-right
                .attr("dy", ".9em") // vertical-align: middle
                .attr("text-anchor", "end") // text-align: right
                .attr("class", "inbar")
                .text(function(d) { return getval(d);});


    chart.selectAll("text.division-title")
            .data(data)
         .enter()
            .append("text")
                .attr("x", 0)
                .attr("y", function(d, i) { return y(i); })
                .attr("dx", -3)
                .attr("dy", ".9em")
                .attr("text-anchor", "end")
                .attr("class", "division-title")
                .text(function(d) { return getname(d);});

    chart.selectAll("line")
            .data(x.ticks(10))
         .enter()
            .append("line")
                .attr("x1", x)
                .attr("x2", x)
                .attr("y1", 0)
                .attr("y2", height)
            .style("stroke", "#ddd");

    chart.selectAll(".rule")
            .data(x.ticks(10))
         .enter()
            .append("text")
                .attr("class", "rule")
                .attr("x", x)
                .attr("y", 0)
                .attr("dy", -3)
                .attr("text-anchor", "middle")
                .text(String);

    chart.append("line")
        .attr("y1", 0)
        .attr("y2", height)
        .style("stroke", "#000");

    redraw();

    function redraw() {
        chart.selectAll("rect")
            .transition()
            .duration(750)
            .attr("width", x);
    };
}

d3.json('{% url "stats:users_by_division_json" %}', drawBarChart);
