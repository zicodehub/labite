import { Formik } from 'formik';
import { useEffect } from 'react';
import { useState } from 'react';
import { Form, Modal, Row, Col, Button, Spinner, Table } from 'react-bootstrap';
import TextInput from '../TextInput';
import SelectInput from '../SelectInput';
import { Client, Fournisseur } from '../constants';
import { deleteCommande, deleteFournisseur, deleteVehicule } from 'components/api';


export default ({open, hide, onCreate, list_vehicules, setVehicules}) => {
    const [ isLoading, setIsLoading ] = useState(false)
  const handleDelete = (id) => deleteVehicule(id).then(() => setVehicules( prev => prev.filter( c => c.id != id)))
    useEffect(() => {

    }, [setIsLoading])

    return (
      <>
        <Modal show={open} onHide={hide} size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered  >
            <Modal.Header closeButton={true}  >
                <Modal.Title>Liste des Véhicules ({list_vehicules.length}) </Modal.Title>
            </Modal.Header>
            <Modal.Body>
         
              <Table striped bordered hover>
                <thead>
                <tr>
                  <th>Dépot</th>
                  <th>Nom</th>
                  <th>Cout</th>
                  <th>Compartiment</th>
                  <th>Taille par compartiment</th>
                  <th>Capacité totale</th>
                </tr>
                </thead>

                <tbody>
                  {list_vehicules.length == 0 && <h3>Aucun véhicule actuellement</h3>}
                  {
                    list_vehicules.map(
                      v => (
                        <tr>
                          <td>D{v.depot_id}</td>
                          <td>{v.name}</td>
                          <td>{v.cout}</td>
                          <td>{v.nb_compartment}</td>
                          <td>{v.size_compartment}</td>
                          <td>{v.size_compartment *v.nb_compartment}</td>
                          <td > 
                            <Button onClick={() => handleDelete(v.id)} className='btn btn-xs btn-danger' >
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
  