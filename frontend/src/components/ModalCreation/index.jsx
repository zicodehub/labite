import { Formik } from 'formik';
import { useEffect } from 'react';
import { useState } from 'react';
import { Form, Modal, Row, Col, Button, Spinner } from 'react-bootstrap';
import TextInput from '../TextInput';
import SelectInput from '../SelectInput';
import { Client, Fournisseur } from '../constants';


export default ({open, hide, coords, onCreate}) => {
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
                time_interval_end: 0
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
  