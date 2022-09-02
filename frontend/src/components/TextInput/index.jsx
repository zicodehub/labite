import React from 'react';
import ReactDOM from 'react-dom';
import { Formik, useField } from 'formik';
import {Form as BForm} from 'react-bootstrap/'


 const TextInput = ({ label, hideError, ...props }) => {

    // useField() returns [formik.getFieldProps(), formik.getFieldMeta()]
    // which we can spread on <input>. We can use field meta to show an error
    // message if the field is invalid and it has been touched (i.e. visited)
 
    const [field, meta] = useField(props);
    // console.log(props.name, field.value)
    
    return (
        <BForm.Group className="mb-3" >
            {label}
            <BForm.Group className="input-group">
                {
                    props.leftPrepand && (
                        <div className="input-group-prepend">
                            {props.leftPrepand}  
                        </div>
                    )
                }
                <BForm.Control  {...field} {...props} className="form-control" />
                {
                    props.rightPrepand && (
                        <div className="input-group-prepend">
                           {props.rightPrepand} 
                        </div>
                    )
                }
            </BForm.Group>
            {  meta.touched && meta.error && meta.error.length > 1 && !hideError ? (
             <BForm.Text className="text-danger">{meta.error}</BForm.Text>
    
        ) : null}
        </BForm.Group>
    );
 
  };
 
  export default TextInput;