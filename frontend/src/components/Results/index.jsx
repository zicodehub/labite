import CarSelectionBox from "../CarSelectionBox"
import Flow from "../Flow"
import Map from "../Map"
import ModalCreation from "../ModalCreation"
import { useState } from "react"
import { Col, Row, Container, Form, Image } from "react-bootstrap"
import MapImage from './map.png'
import Vis from "../Vis"
import { Client, Fournisseur } from "../constants"
const Results = () => {
    const [cars, setCars] = useState([
        {
            name: "V1"
        },
        {
            name: "V2"
        },
        {
            name: "V3"
        },
    ])
    const [ clients, setClients ] = useState([
        // {id: 1,  shape: 'triangle', label:"1", x:0, y:10},
        // {id: 2,  shape: ' hexagon', label:"1", x:0, y:100},
    ])

    const [clickCoords, setClickCoords] = useState({ x: 0, y: 0 })
    const [isOpen, setIsOpen] = useState(false)

    return (
        <Container style={StyleSheet.container} className="mt-5" >
            <ModalCreation open={isOpen} hide={setIsOpen} onCreate={(values) => {
                setClients(prev => {
                    const id = prev.length
                    prev.push({
                        id: id,
                        label: `${ values.node_type == Client ? 'C' : 'F' }${id}`,
                        title: `${ values.node_type == Client ? 'C' : 'F' }${id}`,
                        shape: values.node_type == Client ? 'circle' : 'box',
                        x: Math.random()*10,
                        y: Math.random()*10,
                        color: {
                            background: values.node_type == Client ? 'yellow' : 'red',
                            hover: {
                                border: 'white',
                                background: 'gray'
                            },
                        },
                        font: {
                            color: values.node_type == Client ? 'black' : 'white'
                        },
                        borderWidth: 0
                        
                    })
                    return prev
                })
                console.log(clients)
                setIsOpen(false)
            }} />
            <Row>
                <Col md="1">
                    <CarSelectionBox cars={cars} />
                </Col>
                <Col md="10" className="border" style={{ height: '90vh' }} onDoubleClick={({ pageX, pageY })=> {
                        setClickCoords({ x: pageX, y: pageY })
                        setIsOpen(true)
                        console.log(pageX, pageY)
                     } } >
                    <Vis nodes={clients} />
                    {/* <Image width="100%" height="100%" src={MapImage}  /> */}
                </Col>
                <Col md="1">
                    <p>Détails</p>
                </Col>
            </Row>
        </Container>
    )
}

const styles = {
    container: {

    }
}

export default Results