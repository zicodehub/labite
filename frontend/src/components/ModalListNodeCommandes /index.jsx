import { Formik } from 'formik';
import { useEffect } from 'react';
import { useState } from 'react';
import { Form, Modal, Row, Col, Button, Spinner, Table } from 'react-bootstrap';
import TextInput from '../TextInput';
import SelectInput from '../SelectInput';
import { Client, Depot, Fournisseur } from '../constants';
import { deleteClient, deleteCommande, deleteDepot, deleteFournisseur } from 'components/api';


export default ({open, hide, onCreate, node, list_commandes, setCommandes, setClients, setFournisseurs, setDepots}) => {
  
  // const list_commandes = node.commandes
  console.log(node)

  const [ isLoading, setIsLoading ] = useState(false)

  const handleDeleteCommande = (id) => deleteCommande(id).then(() => setCommandes( prev => prev.filter( c => c.id != id)))
  const handleDeleteNode = () => {
    const id = node.pk
    if(node.node_type == Client) deleteClient(id).then(() => setClients( prev => prev.filter( c => c.id != id)))
    if(node.node_type == Fournisseur) deleteFournisseur(id).then(() => setFournisseurs( prev => prev.filter( c => c.id != id)))
    if(node.node_type == Depot) deleteDepot(id).then(() => setDepots( prev => prev.filter( c => c.id != id)))
    hide()
  }
    
  useEffect(() => {

    }, [setIsLoading])

    return (
      <>
        <Modal show={open} onHide={hide} size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered  >
            <Modal.Header closeButton={true}  >
                <h1>Les commandes associées à {node.name}  <br />({list_commandes.length} commandes) </h1>
            </Modal.Header>
            <Modal.Body>
         
                   
              {/* <h1>Commandes </h1> */}
              <Button className='btn-danger m-2' onClick={handleDeleteNode} >Supprimer ce noeud</Button>
              <Table striped bordered hover>
                <thead>
                <tr>
                  <th>Client</th>
                  <th>Fournisseur</th>
                  <th>Qté commandée</th>
                  <th>Qté livrée</th>
                </tr>
                </thead>

                <tbody>
                  {list_commandes.length == 0 && <h6>Aucune commande actuellement</h6>}
                  {
                    list_commandes.map(
                      order => (
                        <tr className={`${order.qty_fixed == order.qty ? 'bg-warning' : 'bg-success'}`} >
                          <td>C{order.client_id}</td>
                          <td>F{order.fournisseur_id}</td>
                          <td>{order.qty_fixed}</td>
                          <td>{order.qty_fixed - order.qty}</td>
                          <td > <Button onClick={() => handleDeleteCommande(order.id)} className='btn btn-xs btn-danger' >Supprimer</Button></td>
                        </tr>
                      )
                    )
                  }

                </tbody>
              </Table>
              
            </Modal.Body>
            
        </Modal>
      </>
    );
  }
  