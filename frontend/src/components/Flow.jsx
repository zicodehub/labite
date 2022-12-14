import ReactFlow, { MiniMap, Controls } from 'react-flow-renderer';

function Graphical({ nodes, edges, onNodesChange, onEdgesChange, onConnect }) {
    const initialNodes = [
        {
          id: '1',
          type: 'input',
          data: { label: 'Input Node' },
          position: { x: 250, y: 25 },
        },
      
        {
          id: '2',
          // you can also pass a React component as a label
          data: { label: <div>Default Node</div> },
          position: { x: 100, y: 125 },
        },
        {
          id: '3',
          type: 'output',
          data: { label: 'Output Node' },
          position: { x: 250, y: 250 },
        },
      ];
      
      const initialEdges = [
        {  id: 1, source: '1', target: '2' },
        {  id: 2, source: '2', target: '3', animated: true },
        {  id: 3, source: '2', target: '3', animated: false },
      ];
      
  return (
    <ReactFlow
      nodes={initialNodes}
      edges={initialEdges}
    //   onNodesChange={onNodesChange}
    //   onEdgesChange={onEdgesChange}
    //   onConnect={onConnect}
    >
      <MiniMap />
      <Controls />
    </ReactFlow>
  );
}

export default Graphical