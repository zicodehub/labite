import { Formik } from 'formik';
import { useEffect } from 'react';
import { useState } from 'react';
import { Form, Modal, Row, Col, Button, Spinner } from 'react-bootstrap';
import TextInput from '../TextInput';
import SelectInput from '../SelectInput';
import { Client, Fournisseur } from '../constants';


export default ({open, hide, onCreate, list_depots= []}) => {
    const [ isLoading, setIsLoading ] = useState(false)

    useEffect(() => {

    }, [setIsLoading])

    return (
      <>
        <Modal show={open} onHide={hide} size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered  >
            <Modal.Header closeButton={true}  >
                <Modal.Title>Formulaire de création de dépot</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Formik initialValues={{
                name: "",
                x: '',
                y: ''
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
                      
                      <TextInput disabled label="Nom du dépot" name="name" value={`D${list_depots.length+1}`} formik={formik} />

                      <Row>
                          <TextInput label="Longiude x" name="x"  formik={formik} />
                          <TextInput label="Latitude y" name="y"  formik={formik} />
                      </Row>
                     
                      {
                        isLoading ? <Spinner animation="grow" /> : <Button onClick={formik.handleSubmit}>Enregistrer</Button>  
                      }
                      
                    </Form>
                  )
                }
              </Formik>
              <h1>Dépots existant ({list_depots.length}) </h1>
              <Row className='ml-4' style={{marginLeft: 10}} >
                {
                  list_depots.map(
                    p => <Col md="3" className=' bg-warning d-flex' style={{
                      marginRight: 5,
                      marginBottom: 3,
                      fontSize: 18,
                      borderRadius: 10,
                      alignSelf: 'center',
                      textAlign: 'center'

                    }} ><p>{p.name}</p></Col>
                  )
                }
              </Row>
            </Modal.Body>
            
        </Modal>
      </>
    );
  }
  