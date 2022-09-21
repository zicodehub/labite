import { Col, Row, Container, Form } from "react-bootstrap"
import CheckInput from "../CheckInput"
import { Formik } from 'formik';
import { useState } from "react";

const CarSelectionBox = ({ edges = [{v: "V10"}], cars = [], selectedEdges = [], selectedCars, setSelectedCars, setSelectedEdges }) => {
    // const [selected_cars, set_selected_cars] = useState([])
    let formik = null;
    const setFormik = (f) => {
        formik = f
        return 
    }
    const update = async (val) => {
        await formik.setFieldValue('car', val )
        let choice_cars = cars.filter((e, i) =>   val[i] == true )
        // console.log("Selected cars now ", choice_cars.map(c => c.name))
        let concated_edges = []
        choice_cars.forEach( c => {
            let for_c = edges.filter( e => e.v == c.name )
            concated_edges = concated_edges.concat(for_c)
        })
        
        setSelectedEdges(prev => concated_edges)
        setSelectedCars(prev => choice_cars)
        console.log(choice_cars)
    }
return (
        <Form className="border" >
            <h4>Véhicules</h4>
             <Formik initialValues={{
                cars: edges.map(e => cars.find( car => e.v == car.name ))
              }} >
                {
                    formik => (
                        <>
                            
                            {
                                setFormik(formik)
                            }
                            {
                            cars.map( (car, index) => (
                               <>
                                <CheckInput
                                    key={index}
                                    disabled={!edges.find( e => e.v == car.name )}
                                    name={`cars.${index}`}
                                    label={car.name}
                                    formik={formik}
                                    onChange={async () => {
                                        let val = formik.values.cars
                                        val[index] = !val[index]
                                        update(val)
                                        
                                    }}
                                />
                               </>
                            ) )
                        }
                        </>
                    )
                }
              </Formik>
            


    </Form>
    )
}


export default CarSelectionBox