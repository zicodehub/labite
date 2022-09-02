import React from "react";
import ReactDOM from "react-dom";
import Graph from "react-graph-vis";
import "./styles.css";

// need to import the vis network css in order to show tooltip
// import "./network.css";

function Vis({ nodes = [] }) {
  const graph = {
    nodes: nodes,
    edges: []
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

  console.log("vis", nodes)
  
  const events = {
    select: function(event) {
      var { nodes, edges } = event;
      console.log(nodes)
    }
  };
  
  return (
    <Graph
      key={new Date()}
      graph={graph}
      options={options}
      events={events}
      getNetwork={network => {
        //  if you want access to vis.js network api you can set the state in a parent component using this property
      }}
      
    />
  );
}

export default Vis