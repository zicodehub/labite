import React from 'react';
import ReactDOM from 'react-dom';
import {useField } from 'formik';
import {Form as BForm} from 'react-bootstrap/';


 

const SelectInput = ({ label, ...props }) => {

    const [field, meta] = useField(props);
 
    return (
        <BForm.Group className="mb-3" >
        <BForm.Label>{label}</BForm.Label>
        <BForm.Select  {...field} {...props}  />
        {meta.touched && meta.error ? (
         <BForm.Text className="text-muted">{meta.error}</BForm.Text>

    ) : null}
        </BForm.Group>
    );
  };
 
  export default SelectInput;