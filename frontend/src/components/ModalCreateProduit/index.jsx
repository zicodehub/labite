import { Formik } from 'formik';
import { useEffect } from 'react';
import { useState } from 'react';
import { Form, Modal, Row, Col, Button, Spinner } from 'react-bootstrap';
import TextInput from '../TextInput';
import SelectInput from '../SelectInput';
import { Client, Fournisseur } from '../constants';


export default ({open, hide, onCreate, list_types= [], list_produits= []}) => {
    const [ isLoading, setIsLoading ] = useState(false)

    useEffect(() => {

    }, [setIsLoading])

    return (
      <>
        <Modal show={open} onHide={hide} size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered  >
            <Modal.Header closeButton={true}  >
                <Modal.Title>Formulaire de création de produit</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Formik initialValues={{
                type: 1,
                name: ""
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
                      <SelectInput required name="type" label= "Le type du produit" formik={formik} >
                        {
                          list_types.map(
                            t => <option value={t.id}>{t.name}</option>
                          )
                        } 
                      </SelectInput>
                      {/* {console.log(formik.values)} */}
                      <TextInput label="Nom du produit" name="name"  formik={formik} />
                     
                      {
                        isLoading ? <Spinner animation="grow" /> : <Button onClick={formik.handleSubmit}>Enregistrer</Button>  
                      }
                      
                    </Form>
                  )
                }
              </Formik>
              <h1>Produits existant ({list_produits.length}) </h1>
              <Row className='ml-4' style={{marginLeft: 10}} >
                {
                  list_produits.map(
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
  