import { Formik } from 'formik';
import { useEffect } from 'react';
import { useState } from 'react';
import { Form, Modal, Row, Col, Button, Spinner, Table } from 'react-bootstrap';
import TextInput from '../TextInput';
import SelectInput from '../SelectInput';
import { Client, Fournisseur } from '../constants';
import { deleteCommande } from 'components/api';


export default ({open, hide, onCreate, list_commandes, setCommandes}) => {
    const [ isLoading, setIsLoading ] = useState(false)
  const handleDelete = (id) => deleteCommande(id).then(() => setCommandes( prev => prev.filter( c => c.id != id)))
    useEffect(() => {

    }, [setIsLoading])

    return (
      <>
        <Modal show={open} onHide={hide} size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered  >
            <Modal.Header closeButton={true}  >
                <Modal.Title>Liste des commandes ({list_commandes.length}) </Modal.Title>
            </Modal.Header>
            <Modal.Body>
         
                   
              <h1>Commandes </h1>
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
                  {list_commandes.length == 0 && <h3>Aucune commande actuellement</h3>}
                  {
                    list_commandes.map(
                      order => (
                        <tr className={`${order.qty_fixed == order.qty ? 'bg-warning' : 'bg-success'}`} >
                          <td>C{order.client_id}</td>
                          <td>F{order.fournisseur_id}</td>
                          <td>{order.qty_fixed}</td>
                          <td>{order.qty_fixed - order.qty}</td>
                          <td > <Button onClick={() => handleDelete(order.id)} className='btn btn-xs btn-danger' >Supprimer</Button></td>
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
  