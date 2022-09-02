import { Col, Row, Container, Form } from "react-bootstrap"

const CarSelectionBox = ({ cars = [] }) => {
    return (
        <Form className="border" >
            {
                cars.map( car => (
                    <Form.Check 
                    type='checkbox'
                    label={car.name}
                />
                ) )
            }


    </Form>
    )
}


export default CarSelectionBox