import {useCallback} from 'react';
import {useDispatch} from 'react-redux';
// import useCountValue from './selectors';
import {LOGIN, LOGOUT} from './actionTypes';

const useLogin = (payload) => {
  const dispatch = useDispatch();
//   const count = useCountValue();
    dispatch({type: LOGIN, payload});
}

//   return useCallback(() => {
   
//   }, [count, dispatch]);
// };
const useLogout = (payload) => {
    const dispatch = useDispatch();
    //   const count = useCountValue();
    dispatch({
      type: LOGIN,
      payload,
    });
    }
//     return useCallback(() => {
//     }, [count, dispatch]);
//   };
  

export {useLogin, useLogout};