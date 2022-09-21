import React, { useMemo } from "react";
import ReactDOM from "react-dom";
import Graph from "react-graph-vis";
import "./styles.css";
import { Client, Depot, Fournisseur } from "../constants";
// need to import the vis network css in order to show tooltip
// import "./network.css";

function Vis({ nodes = [], edges = [] }) {
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


        // x: index,
        // y: index,
        
        x: n.x,
        y: n.y,
        
        
        shape: n.node_type == Client ? 'circle' : 'box',
        color: {
            background: n.node_type == Client ? 'yellow' : n.node_type == Depot ? 'green' : 'red',
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
    edges: edges
  };

  const options = {
    layout: {
      hierarchical: false
    },
    edges: {
      color: "#000000",
      width: 4
    },
    height: "100%",
    interaction: {
      dragNodes: false,// do not allow dragging nodes
      zoomView: true, // do not allow zooming
      dragView: true,  // do not allow dragging
      navigationButtons: true,
      hover: true
    },
    physics: {
      stabilization: false,
      repulsion: {
        nodeDistance: 0
      },
      maxVelocity: 10
    }
  };

  // console.log("new nodes", graph.nodes)
  
  const events = {
    select: function(event) {
      var { nodes, edges } = event;
      nodes.forEach(
        node_id => {
          const selected_node = graph.nodes.find( n_ => n_.id == node_id )
          console.log("select ", selected_node.name, {x: selected_node.x, y: selected_node.y} )
          
        }
      )
    },
    dragEnd: function(event) {
      var { nodes, edges } = event;
      console.log("dragEnd", event)
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