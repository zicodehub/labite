import React from 'react';
import ReactDOM from 'react-dom';
import {useField } from 'formik';
import {Form as BForm} from 'react-bootstrap/';


const CheckInput = ({ children,label, ...props }) => {
  //TODO: check that @marcleord
    const [field, meta, helpers] = useField({ ...props, type: "checkbox" });
    const validateCheckbox=(helpers, value)=>{
        let error;
      if( value){
        return error
      }
      else{
        return 'le checkbox est incorrect'
      }
    }


    return (

        <BForm.Group className="" >
        <BForm.Check  {
            ...{...field}
            } 
            {...props} label={label}  />
        {children}
        {meta.touched && meta.error ? (
         <BForm.Text className="text-muted">{meta.error}</BForm.Text>

    ) : null}
        </BForm.Group>

    );
  };

export default CheckInput;