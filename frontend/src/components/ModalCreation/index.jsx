import { Formik } from 'formik';
import { useEffect } from 'react';
import { useState } from 'react';
import { Form, Modal, Row, Col, Button, Spinner } from 'react-bootstrap';
import TextInput from '../TextInput';
import SelectInput from '../SelectInput';
import { Client, Fournisseur } from '../constants';


export default ({open, hide, coords, produits, onCreate, fournisseurs}) => {
    const [ isLoading, setIsLoading ] = useState(false)

    useEffect(() => {

    }, [setIsLoading])

    return (
      <>
        <Modal show={open} onHide={hide} size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered  >
            <Modal.Header closeButton={true}  >
                <Modal.Title>Formulaire de création</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Formik initialValues={{
                node_type: Client,
                time_service: 0,
                time_interval_start: 0,
                time_interval_end: 0,
                orders: [{
                  
                }]
              }}
              onSubmit={(values, { setSubmitting , resetForm, ...theremaining}) => {
                if (onCreate) {
                  onCreate(values)
                  console.log(values)
                  }
              }}  >
                {
                  (formik) => (
                    <Form>
                      <SelectInput name="node_type" label= "Tyoe de noeud" formik={formik} >
                          <option value={Client} >Client</option>
                          <option value={Fournisseur}>Fournisseur</option>
                      </SelectInput>
                      {/* {console.log(formik.values)} */}
                      <TextInput label="Temps de service" name="time_service" type='number' formik={formik} />
                      <Row>
                        <Col>
                           <TextInput label="Heure min" name="time_interval_start" type='number' formik={formik} />
                        </Col>
                        <Col>
                           <TextInput label="Heure max" name="time_interval_end" type='number' formik={formik} />
                        </Col>
                      </Row>
                     {
                      (formik.values.node_type === Fournisseur) ? (
                        <Row>
                        {/* {
                          produits.map( p => <TextInput label={p.name} name={"produit."+p.id} type='number' formik={formik} /> )
                        } */}
                      </Row>
                      ) : (
                        <Col>
                          {
                            formik.values.orders.map( (order, index) => (
                              <Row>
                                <Col md="3">
                                  <SelectInput required name={`orders[${index}].fournisseur`} label= "Commander chez" formik={formik} >
                                    <option >Sélection...</option> 
                                      {
                                        fournisseurs.map( f => <option value={f.id} >{f.name}</option> )
                                      }
                                  </SelectInput>
                                </Col>
                                <Col md="4">
                                  <SelectInput required name={`orders[${index}].produit`} label= "Sélection du produit" formik={formik} >
                                      <option >Sélection...</option> 
                                      {
                                        produits.map( p => <option value={p.id} >{p.name}</option> )
                                      }
                                  </SelectInput>
                                </Col>
                                <Col md="3">
                                    <TextInput required label="Quantité" name={`orders[${index}].qty`} type='number' formik={formik} />
                                </Col>
                            </Row>
                            ) )
                          }
                          <Col md="3">
                            <Button onClick={()=> { formik.values.orders.push({}) ; formik.setFieldValue('orders', formik.values.orders); console.log(formik.values.orders)} } >Autre commande</Button>
                          </Col>
                        </Col>
                      )
                     }
                      {
                        isLoading ? <Spinner animation="grow" /> : <Button onClick={formik.handleSubmit}>Enregistrer</Button>  
                      }
                      
                    </Form>
                  )
                }
              </Formik>
            </Modal.Body>
            
        </Modal>
      </>
    );
  }
  