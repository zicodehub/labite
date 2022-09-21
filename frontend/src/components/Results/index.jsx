import CarSelectionBox from "../CarSelectionBox"
import Flow from "../Flow"
import Map from "../Map"
import ModalCreation from "../ModalCreation"
import { useState } from "react"
import { Col, Row, Container, Button, Image, Spinner, Accordion } from "react-bootstrap"
import MapImage from './map.png'
import Vis from "../Vis"
import { Client, Depot, Fournisseur } from "../constants"
import { useEffect } from "react"

import { listClients, runAlgo, listFournisseurs, listVehicules, createClient, listProduits, createFournisseur, createCommande, listDepots, createVehicule, listTypesProduits, createProduit } from "../api"
import ModalCreateVehicule from "components/ModalCreateVehicule"
import ModalCreateProduit from "components/ModalCreateProduit"

const Results = () => {
    const [cars, setCars] = useState([])
    const [selectedEdges, setSelectedEdges] = useState({})
    const [selectedCars, setSelectedCars] = useState({})
    const [trajet_final, setTrajet_final] = useState({})
    const [ clients, setClients ] = useState([])
    const [ depots, setDepots ] = useState([])
    const [ types, setTypes ] = useState([])

    const [ fournisseurs, setFournisseurs ] = useState([])
    const [ produits, setProduits ] = useState([])
    const [ edges, setEdges ] = useState({})

    const [clickCoords, setClickCoords] = useState({ x: 0, y: 0 })
    const [isModalNodeOpen, setModalNode] = useState(false)
    const [isModalVehiculeOpen, setModalVehicule] = useState(false)
    const [isModalProduitOpen, setModalProduit] = useState(false)
    const [details, setDetails] = useState({})
    const [algoError, setAlgoError] = useState({})
    const [isReady, setIsReady] = useState(false)
    const [isRunning, setIsRunning] = useState(false)
    const [idSolution, setIdSolution] = useState(0)
    const [listIdSolution, setListIdSolution] = useState([])


    useEffect(() => {
        listClients().then(res => {
            setClients(prev => res.data.map( c => {
                c.node_type = Client
                const [x, y] = c.coords.split(';')
                c.x = parseInt(x)
                c.y = parseInt(y)
                return c
            } ))
            listFournisseurs().then( async (res) => {
                await setFournisseurs(prev => res.data.map( f => {
                    f.node_type = Fournisseur
                    const [x, y] = f.coords.split(';')
                    f.x = parseInt(x)
                    f.y = parseInt(y)
                    return f
                } ))

                let typesResponse = await listTypesProduits()
                await setTypes(prev => typesResponse.data)
                
                let produitsResponse = await listProduits()
                await setProduits(prev => produitsResponse.data)
                
                let depotResponse = await listDepots()
                await setDepots(prev => depotResponse.data.map( d => {
                    d.node_type = Depot;
                    const [x, y] = d.coords.split(';')
                    d.x = parseInt(x)
                    d.y = parseInt(y)
                    return d
                } ))
                
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

                        {
                            isModalNodeOpen && (
                                <ModalCreation 
                                    open={isModalNodeOpen} hide={setModalNode} 
                                    onCreate={(values) => {
                                        let create_node = undefined;
                                        let node_setter = undefined;
                                        if(values.node_type == Client){
                                            create_node = createClient
                                            node_setter = setClients
                                            createClient({
                                                time_service: values.time_service,
                                                time_interval_start: values.time_interval_start,
                                                time_interval_end: values.time_interval_end,
                                                coords: `${clickCoords.x};${clickCoords.y}`
                                            }).then(res => {
                                                if(values.orders.length > 0) {
                                                    values.orders.forEach( order => {
                                                        createCommande({
                                                            client_id: res.data.id,
                                                            fournisseur_id: parseInt(order.fournisseur),
                                                            produit_id: parseInt(order.produit),
                                                            qty: parseInt(order.qty),
                                                        })
                                                    })
                                                }
                                                setClients(prev => {
                                                    prev.push({
                                                        ...res.data,
                                                        node_type: values.node_type
                                                    })
                                                    return prev
                                                })
                                                setModalNode(false)
                                            } )
                                        } else if(values.node_type == Fournisseur) {
                                            create_node = createFournisseur
                                            node_setter = setFournisseurs
                                            createFournisseur({
                                                time_service: values.time_service,
                                                time_interval_start: values.time_interval_start,
                                                time_interval_end: values.time_interval_end,
                                                coords: `${clickCoords.x};${clickCoords.y}`
                                            }).then(res => {
                                                setFournisseurs(prev => {
                                                    prev.push({
                                                        ...res.data,
                                                        node_type: values.node_type
                                                    })
                                                    return prev
                                                })
                                                setModalNode(false)
                                            } )
                                        }
                                        
                                    }}
                                    produits={produits}
                                    fournisseurs={fournisseurs}
                                    />
                            )
                        }
                        {
                            isModalVehiculeOpen && (
                                <ModalCreateVehicule 
                                    open={isModalVehiculeOpen} hide={setModalVehicule} 
                                    onCreate={(values) => {
                                        createVehicule(values)
                                        .then(
                                            res => {
                                                setCars(prev =>{
                                                    return prev.concat(res.data)
                                                } )
                                                setModalVehicule(false)
                                            }
                                        )
                                    }}
                                    list_depots={depots}
                                    list_vehicules={cars}
                                    />
                            )
                        }
                        {
                            isModalProduitOpen && (
                                <ModalCreateProduit 
                                    open={isModalProduitOpen} hide={setModalProduit} 
                                    onCreate={(values) => {
                                        createProduit(values)
                                        .then(
                                            res => {
                                                setProduits(prev =>{
                                                    return prev.concat(res.data)
                                                } )
                                                setModalProduit(false)
                                            }
                                        )
                                    }}
                                    list_depots={depots}
                                    list_types={types}
                                    list_produits={produits}
                                    />
                            )
                        }
                        <Row>
                            <Col>
                                <Button className="text-white"
                                    onClick={() => setModalVehicule(true) }
                                    >Ajouter un véhcule</Button>
                            </Col>
                            <Col>
                                <Button className="text-white"
                                    onClick={() => setModalProduit(true) }
                                    >Ajouter un produit</Button>
                            </Col>
                            <Col className="offset-6">
                                <Button className="text-white" onClick={()=> {
                                    setIsRunning(prev => true)
                                    runAlgo()
                                    .then( (res) => {
                                        console.log(res)
                                        let data = res.data
                                        data.forEach(
                                            (solution, solution_index) => {
                                                
                                                setDetails(prev => ({
                                                    ...prev,
                                                    [solution_index]: {
                                                        distance: solution.distance,
                                                        cout: solution.cout,
                                                        nb_vehicules: solution.details.length,
                                                        solution: solution.short.map( d => d + ' - ' )
                                                    }
                                                }))
                                                setEdges( prev => {
                                                    // return Object.keys(data.trajet).map( v => ({ name: v, trajet: data.trajet[v] }) )
                                                    let local_edges = []
                                                    console.log("Genetic ", solution.trajet)
                                                    setTrajet_final(prev => ({...prev, [solution_index]: solution.trajet }))
                                                    Object.keys(solution.trajet).forEach( (key, v_index) => {
                                                        let trajet = solution.trajet[key]
                                                        let i = trajet[0]
                                                        let color = [ 10, 39, 11 ]
            
                                                        for (let index = 1; index < trajet.length; index++) {
                                                            const element = trajet[index];
                                                            local_edges.push({
                                                                from: i.name,
                                                                to: element.name,
                                                                v: key,
                                                                mvt: element.mvt,
                                                                label: key,
                                                                title: key,
                                                                color: {
                                                                    color: `#${color[0]}${color[1]}${color[2]}`,
                                                                    hover: `#${color[0]}${color[1]}${color[2]}`
                                                                },
                                                                width: 4
                                                            })
                                                            i = element
                                                            color[v_index%3] += color[v_index%3] + 30
                                                        }
                                                    } )
                                                    console.log(local_edges)
                                                    setSelectedEdges(prev => ({...prev, [solution_index]: local_edges }))
                                                    return {
                                                        ...prev,
                                                        [solution_index]: local_edges
                                                    }
                                                })
                                            
                                                setListIdSolution(prev => prev.concat([solution_index]) )
                                            }
                                            )
                                        setIsRunning(prev => false)
                                        setAlgoError(prev => ({
                                            error: null                                       
                                        }))
                                    } )
                                    .catch(err => {
                                        setAlgoError(prev => ({
                                            error: err.message                                        
                                        }))
                                        setIsRunning(prev => false)
                                    } )
                                }} >Lancer l'algorithme</Button>
                            </Col>
                        </Row>
                        <Row>
                            <Col md="1">
                                <CarSelectionBox cars={cars} edges={edges[idSolution]} selectedCars={selectedCars} setSelectedCars={setSelectedCars} selectedEdges={selectedEdges} setSelectedEdges={setSelectedEdges} />
                            </Col>
                            <Col md="8" className="border" style={{ height: '80vh' }} 
                                onDoubleClick={({ pageX, pageY })=> {
                                    console.log({x: pageX, y: pageY})
                                    setClickCoords({ x: pageX, y: pageY })
                                    setModalNode(true)
                                    // console.log(pageX, pageY)
                                } } 
                                onClick={({ pageX, pageY })=> {
                                    console.log("layout ", {x: pageX, y: pageY})
                                } } 
                                >
                                <Vis nodes={clients.concat(fournisseurs).concat(depots)} edges={selectedEdges[idSolution]} />
                                {/* <Image width="100%" height="100%" src={MapImage}  /> */}
                                {/* <Flow /> */}
                            </Col>
                            <Col>
                                <p>Détails</p>
                                {
                                    isRunning ? <Spinner animation="grow" /> : (
                                        <Accordion defaultActiveKey="0" onSelect={(val) => {
                                            if(val != null) setIdSolution(val) 
                                            }} >
                                            {
                                                algoError.error ? <h3 className="text-danger text-bold">{algoError.error}</h3> : Object.keys(listIdSolution).map( local_solution_index => (
                                                    <Accordion.Item eventKey={local_solution_index}>
                                                        <Accordion.Header>
                                                            Coût : {details[local_solution_index] && details[local_solution_index].cout}
                                                        </Accordion.Header>
                                                        <Accordion.Body>
                                                            <ul>
                                                                <li>Cout : {details[local_solution_index].cout} </li>
                                                                <li>Distance : {details[local_solution_index].distance} </li>
                                                                <li>Véhicules utilisés : {details[local_solution_index].nb_vehicules} </li>
                                                                <li>Solution <br/><strong>{details[local_solution_index].solution}</strong></li>
                                                                { details.error && <li className="text-danger">Erreur <strong>{details[local_solution_index].error}</strong></li> }
                                                                <li>
                                                                    Détails des véhicules sélectionnées
                                                                    <ul>
                                                                        {
                                                                            cars.map( s => (
                                                                                <li> {s.name}
                                                                                <ul>
                                                                                        <li>Trajet : <strong>{trajet_final[local_solution_index] && trajet_final[local_solution_index][s.name]?.map( (d, ind) => `${d.name}${d.mvt ? '('+d.mvt+')' : ''} ${ind+1 == trajet_final[idSolution][s.name].length ? '' : '- '} ` )}</strong></li>
                                                                                    </ul> 
                                                                                </li>
                                                                            ) )
                                                                        }
                                                                    </ul>
                                                                </li>
                                                            </ul>
                                                        </Accordion.Body>
                                                    </Accordion.Item>
                                                ) )
                                            }
                                        </Accordion>
                                    )
                                }
                                 
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