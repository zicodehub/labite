import React, { useMemo } from "react";
import ReactDOM from "react-dom";
import Graph from "react-graph-vis";
import "./styles.css";
import { Client, Depot, Fournisseur, OFFSET_X, OFFSET_Y, ZO_MAP_HEIGHT, ZO_MAP_WIDTH } from "../constants";
import { Col } from "react-bootstrap";
import Node from "./node";
// need to import the vis network css in order to show tooltip
// import "./network.css";

export default ({ nodes = [], edges = [], refresh, setDisplayNode }) => {
  const graph = {
    // nodes: useMemo(() => nodes, [nodes]),
    nodes: nodes.map( (n, index) => {
      let [x, y] = n.coords.split(";")
      return {
        ...n,
        // id: index,
        pk: n.id,
        id: n.name,
        // label: `${ n.node_type == Client ? 'C' : 'F' }${n.id}`,
        label: n.name,
        title: n.name,


        // x: index,
        // y: index,
        
        x: n.x,
        y: n.y,
        
        
        // x: n.x + OFFSET_X,
        // y: n.y + OFFSET_Y,
        
        shape: n.node_type == Client ? 'circle' : 'box',
        color: {
            background: n.node_type == Client ? 'blue' : n.node_type == Depot ? 'red' : 'green',
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
      dragNodes: true,// do not allow dragging nodes
      zoomView: true, // do not allow zooming
      dragView: true,  // do not allow dragging
      // navigationButtons: true,
      hover: true
    },
    physics: {
      enabled: false,
      stabilization: false,
      repulsion: {
        nodeDistance: 1,
        springLength: 1
      },
      maxVelocity: 0
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
  console.log("render parent ", graph.nodes)
  return (
    <Col id="zomap" className="bg-dark" style={{zIndex: 5, width: ZO_MAP_WIDTH, height: ZO_MAP_HEIGHT}} 
     
    >
      {
        graph.nodes.map(
          (node, index) => <Node key={node.id} index={index} 
                node={node} 
                refresh={refresh} 
                original_nodes={nodes}
                setDisplayNode={setDisplayNode}
                /> 
        )
      }
      
    </Col>
  );
}