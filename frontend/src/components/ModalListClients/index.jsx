import { Formik } from 'formik';
import { useEffect } from 'react';
import { useState } from 'react';
import { Form, Modal, Row, Col, Button, Spinner, Table } from 'react-bootstrap';
import TextInput from '../TextInput';
import SelectInput from '../SelectInput';
import { Client, Fournisseur } from '../constants';
import { deleteClient, deleteCommande, deleteFournisseur } from 'components/api';


export default ({open, hide, onCreate, list_clients, setClients}) => {
    const [ isLoading, setIsLoading ] = useState(false)
  const handleDelete = (id) => deleteClient(id).then(() => setClients( prev => prev.filter( c => c.id != id)))
    useEffect(() => {

    }, [setIsLoading])

    return (
      <>
        <Modal show={open} onHide={hide} size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered  >
            <Modal.Header closeButton={true}  >
                <Modal.Title>Liste des noeuds Client ({list_clients.length}) </Modal.Title>
            </Modal.Header>
            <Modal.Body>
         
              <Table striped bordered hover>
                <thead>
                <tr>
                  <th>Nom</th>
                  <th>Coordonnées</th>
                  <th>Commandes passées</th>
                  <th>Qté totale commandée</th>
                </tr>
                </thead>

                <tbody>
                  {list_clients.length == 0 && <h3>Aucun client actuellement</h3>}
                  {
                    list_clients.map(
                    cClient => (
                        <tr>
                          <td>{cClient.name}</td>
                          <td>{cClient.coords.split(";")}</td>
                          <td>{cClient.commandes.length}</td>
                          <td>{cClient.commandes.reduce((total, current) => total+current.qty_fixed, 0)}</td>
                          <td > 
                            <Button onClick={() => handleDelete(cClient.id)} className='btn btn-xs btn-danger' >
                              Supprimer
                            </Button>
                          </td>
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
  