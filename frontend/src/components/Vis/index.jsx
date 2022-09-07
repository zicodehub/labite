import React, { useMemo } from "react";
import ReactDOM from "react-dom";
import Graph from "react-graph-vis";
import "./styles.css";
import { Client, Fournisseur } from "../constants";
// need to import the vis network css in order to show tooltip
// import "./network.css";

function Vis({ nodes = [] }) {
  const graph = {
    // nodes: useMemo(() => nodes, [nodes]),
    nodes: nodes.map( (n, index) => {
      let [x, y] = n.coords.split(";")
      return {
        ...n,
        // id: index,
        id: n.name,
        // label: `${ n.node_type == Client ? 'C' : 'F' }${n.id}`,
        label: n.name,
        title: n.name,
        x: index,
        y: index,
        shape: n.node_type == Client ? 'circle' : 'box',
        color: {
            background: n.node_type == Client ? 'yellow' : 'red',
            hover: {
                border: 'white',
                background: 'gray'
            },
        },
        font: {
            color: n.node_type == Client ? 'black' : 'white'
        },
        borderWidth: 0
      }
    } ),
    edges: [
      {from: 'C10', to: 'F7'}
    ]
  };

  const options = {
    layout: {
      hierarchical: false
    },
    edges: {
      color: "#000000"
    },
    height: "100%",
    interaction: {
      dragNodes: false,// do not allow dragging nodes
      zoomView: false, // do not allow zooming
      dragView: false,  // do not allow dragging
      navigationButtons: true,
      hover: true
    },
    physics: {

    }
  };

  console.log("new nodes", graph.nodes)
  
  const events = {
    select: function(event) {
      var { nodes, edges } = event;
      console.log("click", nodes)
    }
  };
  
  return (
    <Graph
      key={new Date()}
      graph={graph}
      options={options}
      events={events}
      // getNetwork={network => {
      //   //  if you want access to vis.js network api you can set the state in a parent component using this property
      //   console.log(network)
      // }}
      
    />
  );
}

export default Vis