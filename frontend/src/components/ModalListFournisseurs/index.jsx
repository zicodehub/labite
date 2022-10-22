import { Formik } from 'formik';
import { useEffect } from 'react';
import { useState } from 'react';
import { Form, Modal, Row, Col, Button, Spinner, Table } from 'react-bootstrap';
import TextInput from '../TextInput';
import SelectInput from '../SelectInput';
import { Client, Fournisseur } from '../constants';
import { deleteClient, deleteCommande, deleteFournisseur } from 'components/api';


export default ({open, hide, onCreate, list_fournisseurs, setFournisseurs}) => {
    const [ isLoading, setIsLoading ] = useState(false)
  const handleDelete = (id) => deleteClient(id).then(() => setFournisseurs( prev => prev.filter( c => c.id != id)))
    useEffect(() => {

    }, [setIsLoading])

    return (
      <>
        <Modal show={open} onHide={hide} size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered  >
            <Modal.Header closeButton={true}  >
                <Modal.Title>Liste des noeuds Fournisseurs ({list_fournisseurs.length}) </Modal.Title>
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
                  {list_fournisseurs.length == 0 && <h3>Aucun fournisseur actuellement</h3>}
                  {
                    list_fournisseurs.map(
                    fourn => (
                        <tr>
                          <td>{fourn.name}</td>
                          <td>{fourn.coords.split(";")}</td>
                          <td>{fourn.commandes.length}</td>
                          <td>{fourn.commandes.reduce((total, current) => total+current.qty_fixed, 0)}</td>
                          <td > 
                            <Button onClick={() => handleDelete(fourn.id)} className='btn btn-xs btn-danger' >
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
  