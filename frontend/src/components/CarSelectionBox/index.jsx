import { Col, Row, Container, Form } from "react-bootstrap"

const CarSelectionBox = ({ cars = [] }) => {
    return (
        <Form className="border" >
            {
                cars.map( (car, index) => (
                    <Form.Check 
                    key={index}
                    type='checkbox'
                    label={car.name}
                />
                ) )
            }


    </Form>
    )
}


export default CarSelectionBox