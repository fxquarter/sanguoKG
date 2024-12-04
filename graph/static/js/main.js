// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    var graphData = {{ graph_data |safe }};

    var nodes = graphData.nodes.map(function(node) {
        return {
            id: node.name,
            name: node.name,
            symbolSize: 50,
            camp: node.camp,
            itemStyle: {
                color: node.camp === '蜀国' ? '#1772b4' :
                    (node.camp === '魏国' ? '#7c1823' :
                        (node.camp === '吴国' ? '#ff9900' : '#3c9566'))
            },
            label: {
                show: true,  // Show the label
                position: 'inside',  // Position the label inside the node
                formatter: '{b}'  // Display the name of the node
            },
            draggable: true  // Enable node dragging
        };
    });

    var links = graphData.edges.map(function(edge) {
        return {
            source: edge.source,
            target: edge.target,
            value: edge.relation || 'undefined',  // Use relationship type as label
            label: {
                show: true,  // Show the label on the edge
                formatter: edge.relation || 'undefined',  // Display the relationship type
                position: 'middle',  // Position the label in the middle of the edge
                fontSize: 12  // Font size of the label
            },
            lineStyle: {
                width: 2,
                color: 'source',
                curveness: 0.2  // Adds a slight curve to the edge
            },
            // Add arrow to the edge
            symbol: ['none','arrow'],
            symbolSize: [10, 15],  // Size of the arrow
        };
    });

    var myChart = echarts.init(document.getElementById('main'));

    var option = {
        tooltip: {
            trigger: 'item',
            formatter: function(params) {
                if (params.dataType === 'node') {
                    return 'Node: ' + params.data.name + '<br/>Camp: ' + params.data.camp;
                } else if (params.dataType === 'edge') {
                    return 'Relationship: ' + params.data.value;
                }
            }
        },
        animation: true,
        series: [{
            type: 'graph',
            layout: 'force',
            data: nodes,
            links: links,
            roam: true,
            force: {
                repulsion: 1000,  // Repulsion between nodes, higher value means more repulsion
                edgeLength: [50, 150],  // Length of edges
                layoutAnimation: true  // Enable layout animation when nodes are moved
            },
            lineStyle: {
                width: 2,
                color: 'source'
            },
            label: {
                show: true,
                position: 'right',  // Positioning the label on the edge
                fontSize: 12
            }
        }]
    };

    myChart.setOption(option);

    // Add click event listener to nodes
    myChart.on('click', function(params) {
        if (params.dataType === 'node') {
            var personName = params.data.name;
            var personImage = '/static/images/' + personName + '.jpg'; // Assuming image is in 'images' folder
            var personIntroFile = '/static/introduce/' + personName + '.txt'; // Assuming info file is in 'introduce' folder

            // Fetch the introduction text file
            fetch(personIntroFile)
                .then(response => response.text())
                .then(text => {
                    // Update the sidebar content with the image and intro
                    document.getElementById('person-name').innerText = personName;
                    document.getElementById('person-image').src = personImage;
                    document.getElementById('person-intro').innerText = text;

                    // Show the sidebar and overlay
                    document.getElementById('sidebar').style.right = '0';  // Slide in the sidebar
                    document.getElementById('overlay').style.display = 'block'; // Show overlay
                })
                .catch(err => {
                    console.error('Error fetching introduction:', err);
                });
        }
    });

    // Close sidebar when clicking on overlay
    document.getElementById('overlay').addEventListener('click', function() {
        document.getElementById('sidebar').style.right = '-300px'; // Slide out the sidebar
        document.getElementById('overlay').style.display = 'none'; // Hide overlay
    });

    // Filter nodes based on selected faction
    document.getElementById('camp-select').addEventListener('change', function(event) {
        var selectedCamp = event.target.value;

        // Filter nodes based on selected faction
        var filteredNodes = nodes.filter(function(node) {
            if (selectedCamp === 'all') {
                return true;  // Show all nodes if 'all' is selected
            }
            return node.camp === selectedCamp;  // Only show nodes that belong to the selected faction
        });

        // Update chart option with filtered nodes
        myChart.setOption({
            series: [{
                data: filteredNodes
            }]
        });
    });
});
