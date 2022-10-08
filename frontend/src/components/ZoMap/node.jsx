import { updateClient, updateDepot, updateFournisseur } from "components/api";
import { Client, Depot, Fournisseur, NODE_RADIUS, OFFSET_X, OFFSET_Y, ZO_MAP_HEIGHT, ZO_MAP_WIDTH } from "components/constants"
import { useRef, useState } from "react"
import { Overlay, Spinner } from 'react-bootstrap';

export default ({ updateNode, index, original_nodes, refresh, node: props}) => {
    // console.log("rendering node", props.label)

    const [state, setState] = useState({
        ...props,
        isSubmitting: false
    })
    const ref= useRef()
    
    const handleDragStart = () => {
        setState(prev => ({
            ...prev,
            color: {
                ...prev.color,
                background: 'black'
            }
        }))
    }

    const handleDragEnd = (event) => {
        const new_coords = {
            x: event.pageX - OFFSET_X ,
            y: event.pageY - OFFSET_Y
        }
        if(event.pageX + OFFSET_X <= ZO_MAP_WIDTH && event.pageY+OFFSET_Y <= ZO_MAP_HEIGHT) {
            const prev_coords = {
                x: state.x,
                y: state.y
            }
    
            const data = {
                coords: `${new_coords.x};${new_coords.y}`
            }
    
            
            setState(prev => ({
                ...prev,
                color: {
                    ...prev.color,
                    background: props.color.background
                },
                x: new_coords.x,
                y: new_coords.y,
                isSubmitting: true,
                show: false
            }))
    
            if(state.node_type == Client) {
                updateClient(state.pk, data)
                .then(
                    () => setState(prev => ({
                        ...prev,
                        isSubmitting: false
                    }))
                    // () => setTimeout(refresh, 700)
                )
                .catch(err => {
                    console.log(err)
                    // setState(prev => ({
                    //     ...prev,
                    //     x: prev_coords.x,
                    //     y: prev_coords.y,
                    //     isSubmitting: false
                    // }))
                })
                // console.log("update client ", state.pk, data)
            } else if(state.node_type == Fournisseur) {
                updateFournisseur(state.pk, data).then(
                    () => setState(prev => ({
                        ...prev,
                        isSubmitting: false
                    }))
                    // () => null
                    // () => setTimeout(refresh, 700)
                )
                .catch(err => {
                    console.log(err)
                    // setState(prev => ({
                    //     ...prev,
                    //     x: prev_coords.x,
                    //     y: prev_coords.y,
                    //     isSubmitting: false
                    // }))
                })
                // console.log("update fournisseur ", state.pk, new_coords)
            } else if(state.node_type == Depot) {
                updateDepot(state.pk, data).then(
                    () => setState(prev => ({
                        ...prev,
                        isSubmitting: false
                    }))
                    // () => null
                    // () => setTimeout(refresh, 700)
                )
                .catch(err => {
                    console.log(err)
                    // setState(prev => ({
                    //     ...prev,
                    //     x: prev_coords.x,
                    //     y: prev_coords.y,
                    //     isSubmitting: false
                    // }))
                })
            }
    
            // refresh()
            
        }
    }

    return (
        <>
            <div 
                key={state.id}
                ref={ref}
                draggable={true}
                style={{
                    height: NODE_RADIUS,
                    width: NODE_RADIUS,
                    borderRadius: NODE_RADIUS,
                    position: 'absolute', 
                    top: state.y, 
                    left: state.x,
                    backgroundColor: state.color.background,

                    display: 'flex',
                    // cursor: 'move',
                    fontSize: 14,
                    alignContent: 'center',
                    justifyContent: 'center',
                    userSelect: 'none',
                    zIndex: 100,
                }}
                onDragStart={handleDragStart}
                onDragEnd={handleDragEnd}
                onMouseEnter={() => setState(prev => ({...prev, show: true}))}
                onClick={() => setState(prev => ({...prev, show: !prev.show}))}
                onMouseLeave={() => setState(prev => ({...prev, show: false}))}
                // onDragEnter={handleDragStart}

                >
                {state.show && (
                    <div style={{width: 80, position: 'absolute', marginRight: 80}} >
                        <span className="bg-white p-1" style={{fontSize: 20}} >x: {state.x}</span> <br />
                        <span className="bg-white p-1" style={{fontSize: 20}}>y: {state.y}</span>
                    </div>
                )}
                {state.isSubmitting ? <Spinner animation="border" role="status" className='' /> :  <span className="text-white mt-1" style={{fontWeight: 'bold'}} >{state.label}</span>}
            </div>
            
        </>
    )
}