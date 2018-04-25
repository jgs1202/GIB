<template>
<div id="app">
  <input id="checkGroupInABox" type="checkbox">Group in a Box</input>
  <input id="checkShowTreemap" type="checkbox">Show Template</input>
  <select id="selectTemplate" type="select">
      <option value="treemap">Treemap</option>
      <option value="force">Force</option>
    </select>
  <div id="chart"></div>
</div>
</template>

<!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/queue-async/1.0.7/queue.min.js"></script> -->
<script>
const d3 = require('d3')
export default {
  name: 'app',
  data() {
    return {
      msg: 'Welcome to Your Vue.js App',
      force: 0,
      svg: 0,
      width: 1620.7,
      height: 1000,
      color: 0,
      graph: 0,
      useGroupInABox: true,
      drawTemplate: false,
      template: "force",
      node: 0,
      link: 0,
      　
      groupingForce: 0,
      dataNum: 0,
      // mset: [12, 15, 18, 21],
      mset: [12, 15, 18],
      pgroupset: [0, 0.05, 0.1, 0.2],
      poutset: [0, 0.001, 0.002],
      // pgroupset: [0, 0.05, 0.1, 0.2],
      // poutset: [0, 0.0005, 0.001],
      m: 0,
      pgroup: 0,
      pout: 0,
      path: 0,
      dir: 0,
      linkStrength: 0.1,
      intraStrength: 0.2,
      collideForce: -0.2,
      chargeForce: -0.1,
      tempStrength: 0.6,
      radius: 100,
    }
  },
  mounted: function() {
    var that = this
    d3.select("#checkGroupInABox").property("checked", that.useGroupInABox);
    d3.select("#checkShowTreemap").property("checked", that.drawTemplate);
    d3.select("#selectTemplate").property("value", that.template);

    that.color = d3.scaleOrdinal(d3.schemeCategory20)

    that.force = d3.forceSimulation()
      .force("charge", d3.forceManyBody())
      .force("x", d3.forceX(that.width / 2).strength(0.05))
      .force("y", d3.forceY(that.height / 2).strength(0.05));

    that.svg = d3.select("body").append("svg")
      .attr("width", that.width)
      .attr("height", that.height);

    while ((that.poutset[that.pout] == 0) && (that.pgroupset[that.pgroup] == 0)) {
      console.log(that.m, that.pout, that.pgroup)
      that.pout += 1
      if (that.pout == that.poutset.length) {
        that.pout -= that.poutset.length
        that.pgroup += 1
        if (that.pgroup == that.pgroupset.length) {
          that.pgroup -= that.pgroupset.length
          that.m += 1
          if (that.m == that.mset.length) {
            that.force.stop()
          }
        }
      }
      break
    }

    that.reload()
    console.log(that.linkStrength)
    // let stopVar = 0
    // window.onload = function() {
    //   document.getElementById('stopButton').addEventListener('click', clickStop, false)
    // }

    // function clickStop() {
    //   stopVar = 1
    //   // console.log('click')
    // }
  },
  methods: {
    dragstarted: function(d) {
      if (!d3.event.active) force.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    },
    dragged: function(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    },
    dragended: function(d) {
      if (!d3.event.active) force.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    },
    reload: function() {
      console.log('reload')
      var that = this
      //remove all
      that.svg.selectAll(".link").remove();
      that.svg.selectAll(".node").remove();
      that.svg.selectAll(".rect").remove();

      that.force = d3.forceSimulation()
        .force("charge", d3.forceManyBody())
        .force("x", d3.forceX(that.width / 2).strength(0.05))
        .force("y", d3.forceY(that.height / 2).strength(0.05));


      that.dir = './' + '' + that.mset[that.m] + '-' + that.pgroupset[that.pgroup] + '-' + that.poutset[that.pout] + '/'
      that.path = './src/data/' + '' + that.mset[that.m] + '-' + that.pgroupset[that.pgroup] + '-' + that.poutset[that.pout] + '/'
      console.log(that.path, that.dataNum)
      d3.json(that.path + '' + that.dataNum + ".json").then(function(graph) {
        that.graph = graph
        that.groupingForce = that.forceInABox()
          .strength(that.tempStrength) // Strength to foci
          .template(that.template) // Either treemap or force
          .groupBy("group") // Node attribute to group
          .links(graph.links) // The graph links. Must be called after setting the grouping attribute
          .enableGrouping(that.useGroupInABox)
          .nodeSize(5) // How big are the nodes to compute the force template
          .forceCharge(-200) // Separation between nodes on the force template
          .size([that.width, that.height]) // Size of the chart
        // console.log(graph.toString())
        that.force
          .nodes(graph.nodes)
          .force("group", that.groupingForce)
          .force("link", d3.forceLink(graph.links)
            .distance(50)
            // .distance(20)
            .strength(that.groupingForce.getLinkStrength)
          );


        that.link = that.svg.selectAll(".link")
          .data(graph.links)
          .enter().append("line")
          .attr("class", "link")
          .attr('stroke', d3.rgb(150, 150, 150))
          .attr("stroke-width", function(d) {
            // return Math.sqrt(1)
            return 0.3
          });

        that.node = that.svg.selectAll(".node")
          .data(graph.nodes)
          .enter().append("circle")
          .attr("class", "node")
          .attr("r", 5)
          .style("fill", function(d) {
            return d3.interpolateRainbow(d.group / that.mset[that.m]);
          })
          .call(d3.drag()
            .on("start", that.dragstarted)
            .on("drag", that.dragged)
            .on("end", that.dragended));

        that.node.append("title")
          .text(function(d) {
            return d.name;
          });

        that.force.on("tick", function() {
          that.link.attr("x1", function(d) {
              return d.source.x;
            })
            .attr("y1", function(d) {
              return d.source.y;
            })
            .attr("x2", function(d) {
              return d.target.x;
            })
            .attr("y2", function(d) {
              return d.target.y;
            });

          that.node.attr("cx", function(d) {
              return d.x;
            })
            .attr("cy", function(d) {
              return d.y;
            });
        });

        d3.select("#checkGroupInABox").on("change", function() {
          that.force.stop();
          that.useGroupInABox = d3.select("#checkGroupInABox").property("checked");
          that.force
            // .force("link", d3.forceLink(graph.links).distance(50).strength(
            // function (l) { return !useGroupInABox? 0.7 :
            //     l.source.group!==l.target.group ? 0 : 0.1;
            // }))
            .force("group").enableGrouping(that.useGroupInABox)

          that.force.stop()
          that.force.alphaTarget(0.5).restart();
        });

        d3.select("#selectTemplate").on("change", function() {
          that.template = d3.select("#selectTemplate").property("value");
          that.force.stop();
          that.force.force("group").template(that.template);
          that.force.alphaTarget(0.5).restart();
        });
        d3.select("#checkShowTreemap").on("change", function() {
          that.drawTemplate = d3.select("#checkShowTreemap").property("checked");
          if (that.drawTemplate) {
            that.force.force("group").drawTemplate(that.svg);
          } else {
            that.force.force("group").deleteTemplate(that.svg);
          }
        });
      });
    },
    forceInABox: function(alpha) {
      let that = this

      function index(d) {
        return d.index;
      }
      var id = index,
        nodes,
        links, //needed for the force version
        tree,
        size = [100, 100],
        nodeSize = 1, // The expected node size used for computing the cluster node
        forceCharge = -2,
        foci = {},
        // oldStart = force.start,
        linkStrengthIntraCluster = that.intraStrength,
        linkStrengthInterCluster = that.linkStrength,
        // linkStrengthInterCluster = 0.01,
        // oldGravity = force.gravity(),
        templateNodes = [],
        offset = [0, 0],
        templateForce,
        templateNodesSel,
        groupBy = function(d) {
          return d.cluster;
        },
        enableGrouping = true,
        strength = 0.1;
      // showingTemplate = false;

      let groups = [],
        boxes = [],
        data = {}
      // console.log(groups)


      function force(alpha) {
        if (!enableGrouping) {
          return force;
        }
        if (that.template === "force") {
          //Do the tick of the template force and get the new focis
          templateForce.tick();
          getFocisFromTemplate();
        }

        for (var i = 0, n = nodes.length, node, k = alpha * strength; i < n; ++i) {
          node = nodes[i];
          node.vx += (foci[groupBy(node)].x - node.x) * k;
          node.vy += (foci[groupBy(node)].y - node.y) * k;
        }

      }

      function initialize() {
        if (!nodes) return;

        // var i,
        //     n = nodes.length,
        //     m = links.length,
        //     nodeById = map(nodes, id),
        //     link;

        if (that.template === "treemap") {
          initializeWithTreemap();
        } else {
          initializeWithForce();
        }


      }

      force.initialize = function(_) {
        nodes = _;
        initialize();
      };

      function getLinkKey(l) {
        var sourceID = groupBy(l.source),
          targetID = groupBy(l.target);

        return sourceID <= targetID ?
          sourceID + "~" + targetID :
          targetID + "~" + sourceID;
      }

      function computeClustersNodeCounts(nodes) {
        var clustersCounts = d3.map();

        nodes.forEach(function(d) {
          if (!clustersCounts.has(groupBy(d))) {
            clustersCounts.set(groupBy(d), 0);
          }
        });

        nodes.forEach(function(d) {
          // if (!d.show) { return; }
          clustersCounts.set(groupBy(d), clustersCounts.get(groupBy(d)) + 1);
        });

        return clustersCounts;
      }

      //Returns
      function computeClustersLinkCounts(links) {
        var dClusterLinks = d3.map(),
          clusterLinks = [];
        links.forEach(function(l) {
          var key = getLinkKey(l),
            count;
          if (dClusterLinks.has(key)) {
            count = dClusterLinks.get(key);
          } else {
            count = 0;
          }
          count += 1;
          dClusterLinks.set(key, count);
        });

        dClusterLinks.entries().forEach(function(d) {
          var source, target;
          source = d.key.split("~")[0];
          target = d.key.split("~")[1];
          clusterLinks.push({
            "source": source,
            "target": target,
            "count": d.value,
          });
        });
        return clusterLinks;
      }

      //Returns the metagraph of the clusters
      function getGroupsGraph() {
        var gnodes = [],
          glinks = [],
          // edges = [],
          dNodes = d3.map(),
          // totalSize = 0,
          clustersList,
          c, i, size,
          clustersCounts,
          clustersLinks;

        clustersCounts = computeClustersNodeCounts(nodes);
        clustersLinks = computeClustersLinkCounts(links);

        //map.keys() is really slow, it's crucial to have it outside the loop
        clustersList = clustersCounts.keys();
        for (i = 0; i < clustersList.length; i += 1) {
          c = clustersList[i];
          size = clustersCounts.get(c);
          gnodes.push({
            id: c,
            size: size
          });
          dNodes.set(c, i);
          // totalSize += size;
        }

        clustersLinks.forEach(function(l) {
          glinks.push({
            "source": dNodes.get(l.source),
            "target": dNodes.get(l.target),
            "count": l.count
          });
        });


        return {
          nodes: gnodes,
          links: glinks
        };
      }


      function getGroupsTree() {
        var children = [],
          totalSize = 0,
          clustersList,
          c, i, size, clustersCounts;

        clustersCounts = computeClustersNodeCounts(force.nodes());

        //map.keys() is really slow, it's crucial to have it outside the loop
        clustersList = clustersCounts.keys();
        for (i = 0; i < clustersList.length; i += 1) {
          c = clustersList[i];
          size = clustersCounts.get(c);
          children.push({
            id: c,
            size: size
          });
          totalSize += size;
        }
        // return {id: "clustersTree", size: totalSize, children : children};
        return {
          id: "clustersTree",
          children: children
        };
      }


      function getFocisFromTemplate() {
        //compute foci
        foci.none = {
          x: 0,
          y: 0
        };
        templateNodes.forEach(function(d) {
          if (that.template === "treemap") {
            foci[d.data.id] = {
              x: (d.x0 + (d.x1 - d.x0) / 2) - offset[0],
              y: (d.y0 + (d.y1 - d.y0) / 2) - offset[1]
            };
          } else {
            foci[d.id] = {
              x: d.x - offset[0],
              y: d.y - offset[1]
            };
          }
        });
      }

      function initializeWithTreemap() {
        var treemap = d3.treemap()
          .size(force.size());

        tree = d3.hierarchy(getGroupsTree())
          // .sort(function (p, q) { return d3.ascending(p.size, q.size); })
          // .count()
          .sum(function(d) {
            return d.size;
          })
          .sort(function(a, b) {
            return b.height - a.height || b.value - a.value;
          });


        templateNodes = treemap(tree).leaves();

        getFocisFromTemplate();
      }

      function checkLinksAsObjects() {
        // Check if links come in the format of indexes instead of objects
        var linkCount = 0;
        if (nodes.length === 0) return;

        links.forEach(function(alink) {
          var source, target;
          if (!nodes) return;
          source = alink.source;
          target = alink.target;
          if (typeof alink.source !== "object") source = nodes[alink.source];
          if (typeof alink.target !== "object") target = nodes[alink.target];
          if (source === undefined || target === undefined) {
            // console.log(alink);
            throw Error("Error setting links, couldn't find nodes for a link (see it on the console)");
          }
          alink.source = source;
          alink.target = target;
          alink.index = linkCount++;
        });
      }

      function initializeWithForce() {
        var net;

        if (nodes && nodes.length > 0) {
          if (groupBy(nodes[0]) === undefined) {
            throw Error("Couldn't find the grouping attribute for the nodes. Make sure to set it up with forceInABox.groupBy('attr') before calling .links()");
          }
        }

        checkLinksAsObjects();

        net = getGroupsGraph();
        templateForce = d3.forceSimulation(net.nodes)
          .force("x", d3.forceX(size[0] / 2).strength(0.5))
          .force("y", d3.forceY(size[1] / 2).strength(0.5))
          .force("collide", d3.forceCollide(function(d) {
            return d.size * nodeSize * that.collideForce;
          }))
          .force("charge", d3.forceManyBody().strength(function(d) {
            return forceCharge * d.size * that.chargeForce;
          }))
          .force("links", d3.forceLink(!net.nodes ? net.links : []))
          .on('end', onEnd)

        templateForce.force('collide').radius(that.radius)

        templateNodes = templateForce.nodes();

        getFocisFromTemplate();
      }

      function onEnd() {
        // console.log(nodes)
        // console.log(nodes.map(function(d) { return [d.x, d.y] }))
        getCoo()
      }

      function getCoo() {
        // console.log(nodes[73])
        var max = 0
        for (let i = 0; i < nodes.length; i++) {
          if (nodes[i].group > max) {
            max = nodes[i].group
          }
        }
        for (let i = 0; i <= max; i++) {
          groups.push([])
        }
        // console.log(groups)
        for (let i = 0; i < nodes.length; i++) {
          groups[nodes[i].group].push(i)
        }
        // console.log(groups)
        calcBox()
      }

      function calcBox() {
        for (let i = 0; i < groups.length; i++) {
          let ymax = 0,
            ymin = 0,
            xmax = 0,
            xmin = 0;
          for (let j = 0; j < groups[i].length; j++) {
            // console.log(j)
            if (j === 0) {
              ymax = nodes[groups[i][j]].y
              ymin = nodes[groups[i][j]].y
              xmax = nodes[groups[i][j]].x
              xmin = nodes[groups[i][j]].x
            }
            if (nodes[groups[i][j]].y > ymax) {
              ymax = nodes[groups[i][j]].y
              // console.log('ymax')
            }
            if (nodes[groups[i][j]].y < ymin) {
              ymin = nodes[groups[i][j]].y
              // console.log('ymin')
            }
            if (nodes[groups[i][j]].x > xmax) {
              xmax = nodes[groups[i][j]].x
              // console.log('xmax')
            }
            if (nodes[groups[i][j]].x < xmin) {
              xmin = nodes[groups[i][j]].x
              // console.log('xmin')
            }
            if (i === 0) {
              // console.log(nodes[groups[i][j]])
              // console.log(xmax)
            }
          }
          boxes.push([ymin, ymax, xmin, xmax])
        }
        // console.log(boxes)

        data.nodes = nodes
        data.boxes = boxes
        // d3.selectAll("path.line").remove();
        // console.log('links are ')
        // console.log(links)
        // for (let i=0; i<data.boxes.length; i++){
        //   d3.select('#' + '' + i).remove()
        // }
        // console.log(boxes)
        // console.log(typeof data.nodes)
        // console.log(data.nodes)

        //calc unit area
        let area = []
        for (let i = 0; i < data.boxes.length; i++) {
          let ver = data.boxes[i][1] + 5 - data.boxes[i][0] + 5
          let hor = data.boxes[i][3] + 5 - data.boxes[i][2] + 5
          let unit
          if (ver > hor) {
            unit = ver * ver
          } else {
            unit = hor * hor
          }
          // console.log(unit)
          area.push(unit / groups[i].length)
          // console.log(unit)
        }
        let max = area[0]
        for (let i = 0; i < data.boxes.length; i++) {
          if (area[i] > max) {
            max = area[i]
          }
        }
        max = 1000
        // console.log(max, area)
        for (let i = 0; i < area.length; i++) {
          // if (area[i] === max){
          let groupSize = max * groups[i].length
          let side = Math.sqrt(groupSize)
          let cy = (data.boxes[i][1] + data.boxes[i][0]) / 2
          let cx = (data.boxes[i][3] + data.boxes[i][2]) / 2
          // console.log(groupSize, side, cy, cx)

          data.boxes[i][0] = cy - side / 2
          data.boxes[i][1] = cy + side / 2
          data.boxes[i][2] = cx - side / 2
          data.boxes[i][3] = cx + side / 2
          // console.log( (data.boxes[i][1] - data.boxes[i][0])*(data.boxes[i][3] - data.boxes[i][2]) )
          // }
          // else if (area[i] != max){

          // let verify = 0
          // let step = 5
          // while( verify == 0 ){
          //   let heightStep = groupSize / ( data.boxes[i][3] - data.boxes[i][2] + 2 * step )
          //   if ( heightStep <= ( data.boxes[i][1] - data.boxes[i][0] + 2 * (step + 3) ) ) {
          //     data.boxes[i][2] -= step
          //     data.boxes[i][3] += step
          //     let pre0 = data.boxes[i][0]
          //     let pre1 = data.boxes[i][1]
          //     data.boxes[i][0] = pre0 - (heightStep - ( pre1 - pre0 )) /2
          //     data.boxes[i][1] = pre1 + (heightStep - ( pre1 - pre0 )) /2
          //     verify = 1
          //   }
          //   step += 1
          // }
        }



        for (let i = 0; i < data.boxes.length; i++) {
          // let coo = [{ "x": data.boxes[i][2] - 15, "y": data.boxes[i][0] - 15 }, { "x": data.boxes[i][2] - 15, "y": data.boxes[i][1] + 15 },
          //   { "x": data.boxes[i][3] + 15, "y": data.boxes[i][1] + 15 }, { "x": data.boxes[i][3] + 15, "y": data.boxes[i][0] - 15 }, { "x": data.boxes[i][2] - 15, "y": data.boxes[i][0] - 15 }]
          let coo = [{
              "x": data.boxes[i][2],
              "y": data.boxes[i][0]
            }, {
              "x": data.boxes[i][2],
              "y": data.boxes[i][1]
            },
            {
              "x": data.boxes[i][3],
              "y": data.boxes[i][1]
            }, {
              "x": data.boxes[i][3],
              "y": data.boxes[i][0]
            }, {
              "x": data.boxes[i][2],
              "y": data.boxes[i][0]
            }
          ]

          // console.log('coo is ' + '' + coo[0]['x'])
          var lineFunc = d3.line()
            .x(function(d) {
              return d.x;
            })
            .y(function(d) {
              return d.y;
            });
          // console.log(this.svg)
          that.svg.append('path')
            .attr('class', 'rect')
            .attr('d', lineFunc(coo))
            .attr('stroke', 'black')
            .attr('stroke-width', 1)
            .attr('fill', 'none')
          // .attr('id', i)
        }

        // console.log(data.boxes)
        let groupData = []
        for (let corner = 0; corner < data.boxes.length; corner++) {
          let cood = {}
          cood.one = data.boxes[corner][0]
          cood.two = data.boxes[corner][1]
          cood.three = data.boxes[corner][2]
          cood.four = data.boxes[corner][3]
          groupData.push(cood)
        }
        data.boxes = groupData
        data.links = []
        for (let j = 0; j < links.length; j++) {
          let dic = {}
          dic.source = links[j].source.index
          dic.target = links[j].target.index
          dic.value = links[j].value
          data.links.push(dic)
          // console.log(links[j].source)
        }
        console.log(that)
        data.pgroup = that.graph.pgroup
        data.pout = that.graph.pout
        data.groupSize = that.graph.groupSize
        data.dir = that.dir
        data.file = '' + that.dataNum + '.json'
        data.id = that.path + '' + that.dataNum + '.json'
        data.mostConnected = that.graph.mostConnected
        data.nodeMax = that.graph.nodeMax
        data.nodeMin = that.graph.nodeMin
        data.linkMax = that.graph.linkMax
        data.linkMin = that.graph.linkMin
        fetch('http://localhost:3000/coordinates', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        }).then(res => res.json()).then(console.log);
        that.dataNum += 1
        console.log(that.dataNum)
        if (that.dataNum == 10) {
          that.dataNum -= 10
          that.pout += 1
          if (that.pout == that.poutset.length) {
            that.pout -= that.poutset.length
            that.pgroup += 1
            if (that.pgroup == that.pgroupset.length) {
              that.pgroup -= that.pgroupset.length
              that.m += 1
              if (that.m == that.mset.length) {
                that.force.stop()
              }
            }
          }
        }

        while ((that.poutset[that.pout] == 0) && (that.pgroupset[that.pgroup] == 0)) {
          that.pout += 1
          if (that.pout == that.poutset.length) {
            that.pout -= that.poutset.length
            that.pgroup += 1
            if (that.pgroup == that.pgroupset.length) {
              that.pgroup -= that.pgroupset.length
              that.m += 1
              if (that.m == that.mset.length) {
                that.force.stop()
              }
            }
          }
        }

        console.log(data)
        that.reload()
        // downloadFile(data, 'data', 'json')
        // downloadFile(links, 'links', 'json')
        // downloadFile(tableToCsvString(data.boxes), 'boxes', 'csv')
        // console.log('reload is ' + stopVar)

        // if (stopVar != 1) {
        //   reload ()
        // }
      }


      function drawTreemap(container) {
        container.selectAll(".cell").remove();
        container.selectAll(".cell")
          .data(templateNodes)
          .enter().append("svg:rect")
          .attr("class", "cell")
          .attr("x", function(d) {
            return d.x0;
          })
          .attr("y", function(d) {
            return d.y0;
          })
          .attr("width", function(d) {
            return d.x1 - d.x0;
          })
          .attr("height", function(d) {
            return d.y1 - d.y0;
          });

      }

      function drawGraph(container) {
        container.selectAll(".cell").remove();
        templateNodesSel = container.selectAll("cell")
          .data(templateNodes);
        templateNodesSel
          .enter().append("svg:circle")
          .attr("class", "cell")
          .attr("cx", function(d) {
            return d.x;
          })
          .attr("cy", function(d) {
            return d.y;
          })
          .attr("r", function(d) {
            return d.size * nodeSize;
          });

      }

      force.drawTemplate = function(container) {
        // showingTemplate = true;
        if (that.template === "treemap") {
          drawTreemap(container);
        } else {
          drawGraph(container);
        }
        return force;
      };

      //Backwards compatibility
      force.drawTreemap = force.drawTemplate;

      force.deleteTemplate = function(container) {
        // showingTemplate = false;
        container.selectAll(".cell").remove();

        return force;
      };


      force.template = function(x) {
        if (!arguments.length) return that.template;
        that.template = x;
        initialize();
        return force;
      };

      force.groupBy = function(x) {
        if (!arguments.length) return groupBy;
        if (typeof x === "string") {
          groupBy = function(d) {
            return d[x];
          };
          return force;
        }
        groupBy = x;
        return force;
      };


      force.enableGrouping = function(x) {
        if (!arguments.length) return enableGrouping;
        enableGrouping = x;
        // update();
        return force;
      };

      force.strength = function(x) {
        if (!arguments.length) return strength;
        strength = x;
        return force;
      };


      force.getLinkStrength = function(e) {
        if (enableGrouping) {
          if (groupBy(e.source) === groupBy(e.target)) {
            if (typeof(linkStrengthIntraCluster) === "function") {
              return linkStrengthIntraCluster(e);
            } else {
              return linkStrengthIntraCluster;
            }
          } else {
            if (typeof(linkStrengthInterCluster) === "function") {
              return linkStrengthInterCluster(e);
            } else {
              return linkStrengthInterCluster;
            }
          }
        } else {
          // Not grouping return the intracluster
          if (typeof(linkStrengthIntraCluster) === "function") {
            return linkStrengthIntraCluster(e);
          } else {
            return linkStrengthIntraCluster;
          }

        }
      };


      force.id = function(_) {
        return arguments.length ? (id = _, force) : id;
      };

      force.size = function(_) {
        return arguments.length ? (size = _, force) : size;
      };

      force.linkStrengthInterCluster = function(_) {
        return arguments.length ? (linkStrengthInterCluster = _, force) : linkStrengthInterCluster;
      };

      force.linkStrengthIntraCluster = function(_) {
        return arguments.length ? (linkStrengthIntraCluster = _, force) : linkStrengthIntraCluster;
      };

      force.nodes = function(_) {
        return arguments.length ? (nodes = _, force) : nodes;
      };

      force.links = function(_) {
        if (!arguments.length)
          return links;
        if (_ === null) links = [];
        else links = _;
        return force;
      };

      force.nodeSize = function(_) {
        return arguments.length ? (nodeSize = _, force) : nodeSize;
      };

      force.forceCharge = function(_) {
        return arguments.length ? (forceCharge = _, force) : forceCharge;
      };

      force.offset = function(_) {
        return arguments.length ? (offset = _, force) : offset;
      };

      return force;
    },
    tableToCsvString: function(table) {
      var str = '',
        imax, jmax
      for (var i = 0, imax = table.length - 1; i <= imax; ++i) {
        var row = table[i];
        for (var j = 0, jmax = row.length - 1; j <= jmax; ++j) {
          str += '"' + row[j] + '"';
          // str += '"' + row[j].replace('"', '""') + '"';
          // str +=
          if (j !== jmax) {
            str += ',';
          }
        }
        str += '\n';
      }
      // console.log(str)
      return str;
    },
    downloadFile: function(data, name, type) {
      // console.log(data)
      // let sample = { data: 'sample' }
      var bom = new Uint8Array([0xEF, 0xBB, 0xBF]);
      // var content = 'あいうえお,かきくけこ,さしすせそ,aiueo';
      var a = document.createElement('a')
      var blob

      if (type === 'json') {
        blob = new Blob([JSON.stringify(data, null, '  ')], {
          type: 'application\/json'
        })
        a.download = name + '.json'
        console.log('json')
      } else if (type === 'csv') {
        blob = new Blob([data], {
          type: "text/csv"
        });
        // blob = new Blob([bom, data], { type: "text/csv" })
        // blob = new Blob([bom, data], { type: "text/csv" })
        // console.log(data)
        a.download = name + '.csv'
        console.log('csv')
      } else {
        alert('The file type is not valid.')
      }

      a.target = '_blank'
      if (window.navigator.msSaveBlob) {
        // for IE
        window.navigator.msSaveBlob(blob, name)
      } else if (window.URL && window.URL.createObjectURL) {
        // for Firefox
        a.href = window.URL.createObjectURL(blob);
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      } else if (window.webkitURL && window.webkitURL.createObject) {
        // for Chrome
        a.href = window.webkitURL.createObjectURL(blob);
        a.click();
      } else {
        // for Safari
        window.open('data:' + mimeType + ';base64,' + window.Base64.encode(content), '_blank');
      }
      // if (window.navigator.msSaveBlob) {
      //   window.navigator.msSaveBlob(blob, "test.txt");

      //   // msSaveOrOpenBlobの場合はファイルを保存せずに開ける
      //   window.navigator.msSaveOrOpenBlob(blob, "test.txt");
      // } else {
      //   document.getElementById("download").href = window.URL.createObjectURL(blob);
      // }
    },
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1,
h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
