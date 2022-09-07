import CarSelectionBox from "../CarSelectionBox"
import Flow from "../Flow"
import Map from "../Map"
import ModalCreation from "../ModalCreation"
import { useState } from "react"
import { Col, Row, Container, Button, Image, Spinner } from "react-bootstrap"
import MapImage from './map.png'
import Vis from "../Vis"
import { Client, Fournisseur } from "../constants"
import { useEffect } from "react"

import { listClients, listFournisseurs, listVehicules, createClient, listProduits, createFournisseur } from "../api"

const Results = () => {
    const [cars, setCars] = useState([
        // {
        //     name: "V1"
        // },
        // {
        //     name: "V2"
        // },
        // {
        //     name: "V3"
        // },
    ])
    const [ clients, setClients ] = useState([

    ])
    const [ fournisseurs, setFournisseurs ] = useState([])
    const [ produits, setProduits ] = useState([])
    const [ edges, setEdges ] = useState({
        active: [],
        all: []
    })

    const [clickCoords, setClickCoords] = useState({ x: 0, y: 0 })
    const [isOpen, setIsOpen] = useState(false)
    const [isReady, setIsReady] = useState(false)


    useEffect(() => {
        listClients().then(res => {
            setClients(prev => res.data.map( c => {
                c.node_type = Client
                return c
            } ))
            listFournisseurs().then( async (res) => {
                await setFournisseurs(prev => res.data.map( c => {
                    c.node_type = Fournisseur
                    return c
                } ))
                let produitsResponse = await listProduits()
                await setProduits(prev => produitsResponse.data)
                
                let carsResponse = await listVehicules()
                await setCars(prev => carsResponse.data)
                await setIsReady(prev => true)
            })
        })
        
        // listProduits().then(res => setProduits(res.data))
    }, [setCars, setClients, setFournisseurs, setIsReady])

    return (
        <Container style={StyleSheet.container} className="mt-5" >
            {
                !isReady ? <Spinner  animation="grow" /> : (
                    <>

                        <ModalCreation 
                            open={isOpen} hide={setIsOpen} 
                            onCreate={(values) => {
                                let create_node = undefined;
                                let node_setter = undefined;
                                if(values.node_type == Client){
                                    create_node = createClient
                                    node_setter = setClients
                                } else if(values.node_type == Fournisseur) {
                                    create_node = createFournisseur
                                    node_setter = setFournisseurs
                                }
                                create_node({
                                    time_service: values.time_service,
                                    time_interval_start: values.time_interval_start,
                                    time_interval_end: values.time_interval_end,
                                    coords: `${clickCoords.x};${clickCoords.y}`
                                }).then(res => {
                                    node_setter(prev => {
                                        prev.push({
                                            ...res.data,
                                            node_type: values.node_type
                                        })
                                        return prev
                                    })
                                    setIsOpen(false)
                                } )
                            }}
                            
                            />
                        <Row>
                            <Button className="offset-10" >Lancer l'algorithme</Button>
                        </Row>
                        <Row>
                            <Col md="1">
                                <CarSelectionBox cars={cars} />
                            </Col>
                            <Col md="10" className="border" style={{ height: '90vh' }} onDoubleClick={({ pageX, pageY })=> {
                                    setClickCoords({ x: pageX, y: pageY })
                                    setIsOpen(true)
                                    console.log(pageX, pageY)
                                } } >
                                <Vis nodes={clients.concat(fournisseurs)} />
                                {/* <Image width="100%" height="100%" src={MapImage}  /> */}
                            </Col>
                            <Col md="1">
                                <p>Détails</p>
                            </Col>
                        </Row>            
                    </>
            )
        }
    </Container>
    )
}

const styles = {
    container: {

    }
}

export default Results