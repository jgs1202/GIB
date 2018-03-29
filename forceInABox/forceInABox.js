/* global d3 */

function forceInABox(alpha) {
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
    linkStrengthIntraCluster = 0.1,
    linkStrengthInterCluster = 0.01,
    // oldGravity = force.gravity(),
    templateNodes = [],
    offset = [0, 0],
    templateForce,
    templateNodesSel,
    groupBy = function(d) { return d.cluster; },
    template = "treemap",
    enableGrouping = true,
    strength = 0.1;
  // showingTemplate = false;

  let groups = [],
    boxes = [],
    data = {}
  console.log(groups)


  function force(alpha) {
    if (!enableGrouping) {
      return force;
    }
    if (template === "force") {
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

    if (template === "treemap") {
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
      gnodes.push({ id: c, size: size });
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


    return { nodes: gnodes, links: glinks };
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
      children.push({ id: c, size: size });
      totalSize += size;
    }
    // return {id: "clustersTree", size: totalSize, children : children};
    return { id: "clustersTree", children: children };
  }


  function getFocisFromTemplate() {
    //compute foci
    foci.none = { x: 0, y: 0 };
    templateNodes.forEach(function(d) {
      if (template === "treemap") {
        foci[d.data.id] = {
          x: (d.x0 + (d.x1 - d.x0) / 2) - offset[0],
          y: (d.y0 + (d.y1 - d.y0) / 2) - offset[1]
        };
      } else {
        foci[d.id] = { x: d.x - offset[0], y: d.y - offset[1] };
      }
    });
  }

  function initializeWithTreemap() {
    var treemap = d3.treemap()
      .size(force.size());

    tree = d3.hierarchy(getGroupsTree())
      // .sort(function (p, q) { return d3.ascending(p.size, q.size); })
      // .count()
      .sum(function(d) { return d.size; })
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

    links.forEach(function(link) {
      var source, target;
      if (!nodes) return;
      source = link.source;
      target = link.target;
      if (typeof link.source !== "object") source = nodes[link.source];
      if (typeof link.target !== "object") target = nodes[link.target];
      if (source === undefined || target === undefined) {
        console.log(link);
        throw Error("Error setting links, couldn't find nodes for a link (see it on the console)");
      }
      link.source = source;
      link.target = target;
      link.index = linkCount++;
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
      .force("collide", d3.forceCollide(function(d) { return d.size * nodeSize; }))
      .force("charge", d3.forceManyBody().strength(function(d) { return forceCharge * d.size; }))
      .force("links", d3.forceLink(!net.nodes ? net.links : []))
      .on('end', onEnd)

    templateNodes = templateForce.nodes();

    getFocisFromTemplate();
  }

  function onEnd() {
    console.log(nodes)
    console.log(nodes.map(function(d) { return [d.x, d.y] }))
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
    console.log(groups)
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
    console.log(boxes)
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
    console.log(max, area)
    for (let i = 0; i < area.length; i++) {
      // if (area[i] === max){
      let groupSize = max * groups[i].length
      let side = Math.sqrt(groupSize)
      let cy = (data.boxes[i][1] + data.boxes[i][0]) / 2
      let cx = (data.boxes[i][3] + data.boxes[i][2]) / 2
      console.log(groupSize, side, cy, cx)

      data.boxes[i][0] = cy - side/2
      data.boxes[i][1] = cy + side/2
      data.boxes[i][2] = cx - side/2
      data.boxes[i][3] = cx + side/2
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
      let coo = [{ "x": data.boxes[i][2], "y": data.boxes[i][0] }, { "x": data.boxes[i][2], "y": data.boxes[i][1] },
        { "x": data.boxes[i][3], "y": data.boxes[i][1] }, { "x": data.boxes[i][3], "y": data.boxes[i][0] }, { "x": data.boxes[i][2], "y": data.boxes[i][0] }
      ]
      console.log('coo is ' + '' + coo[0]['x'])
      var lineFunc = d3.line()
        .x(function(d) { return d.x; })
        .y(function(d) { return d.y; });
      // console.log(svg)
      svg.append('path')
        .attr('d', lineFunc(coo))
        .attr('stroke', 'black')
        .attr('stroke-width', 1)
        .attr('fill', 'none')
      // .attr('id', i)
    }
    data.links = links
    downloadFile(data, 'data', 'json')
    // downloadFile(links, 'links', 'json')
    downloadFile(tableToCsvString(data.boxes), 'boxes', 'csv')
    console.log('reload is ' + stopVar)

    // if (stopVar != 1) {
    //   reload ()
    // }
  }


  function drawTreemap(container) {
    container.selectAll(".cell").remove();
    container.selectAll("cell")
      .data(templateNodes)
      .enter().append("svg:rect")
      .attr("class", "cell")
      .attr("x", function(d) { return d.x0; })
      .attr("y", function(d) { return d.y0; })
      .attr("width", function(d) { return d.x1 - d.x0; })
      .attr("height", function(d) { return d.y1 - d.y0; });

  }

  function drawGraph(container) {
    container.selectAll(".cell").remove();
    templateNodesSel = container.selectAll("cell")
      .data(templateNodes);
    templateNodesSel
      .enter().append("svg:circle")
      .attr("class", "cell")
      .attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; })
      .attr("r", function(d) { return d.size * nodeSize; });

  }

  force.drawTemplate = function(container) {
    // showingTemplate = true;
    if (template === "treemap") {
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
    if (!arguments.length) return template;
    template = x;
    initialize();
    return force;
  };

  force.groupBy = function(x) {
    if (!arguments.length) return groupBy;
    if (typeof x === "string") {
      groupBy = function(d) { return d[x]; };
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
}

var tableToCsvString = function(table) {
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
};

function downloadFile(data, name, type) {
  // console.log(data)
  // let sample = { data: 'sample' }
  var bom = new Uint8Array([0xEF, 0xBB, 0xBF]);
  // var content = 'あいうえお,かきくけこ,さしすせそ,aiueo';
  var a = document.createElement('a')
  var blob

  if (type === 'json') {
    blob = new Blob([JSON.stringify(data, null, '  ')], { type: 'application\/json' })
    a.download = name + '.json'
    console.log('json')
  } else if (type === 'csv') {
    blob = new Blob([data], { type: "text/csv" });
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
}
