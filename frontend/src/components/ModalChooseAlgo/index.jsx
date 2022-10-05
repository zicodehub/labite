import { Formik } from 'formik';
import { useEffect } from 'react';
import { useState } from 'react';
import { Form, Modal, Row, Col, Button, Spinner } from 'react-bootstrap';
import TextInput from '../TextInput';
import SelectInput from '../SelectInput';
import { Client, Fournisseur } from '../constants';


export default ({open, hide, onCreate}) => {
    const [ isLoading, setIsLoading ] = useState(false)

    useEffect(() => {

    }, [setIsLoading])

    return (
      <>
        <Modal show={open} onHide={hide} size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered  >
            <Modal.Header closeButton={true}  >
                <Modal.Title>Sélection d'un algo</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Formik initialValues={{
                algo: '',
                size_compartment: 10,
                cout: 10,
                depot_id: 1,
              }}
              onSubmit={(values, { setSubmitting , resetForm, ...theremaining}) => {
                if (onCreate) {
                  setIsLoading(true)
                  onCreate(values)
                  console.log(values)
                  }
              }}  >
                {
                  (formik) => (
                    <Form>
                      <SelectInput required name="depot_id" label= "Dépot" formik={formik} >
                        {
                          list_depots.map(
                            d => <option value={d.id}>{d.name}</option>
                          )
                        } 
                      </SelectInput>
                      {/* {console.log(formik.values)} */}
                      <TextInput label="Cout du véhicule" name="cout" type='number' formik={formik} />
                      <Row>
                        <Col>
                            <TextInput label="Nombre de compartiments" name="nb_compartment" type='number' formik={formik} />
                        </Col>
                        <Col>
                            <TextInput label="Taille d'un compartiment" name="size_compartment" type='number' formik={formik} />
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
  