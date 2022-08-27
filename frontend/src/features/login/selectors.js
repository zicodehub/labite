import {useSelector} from 'react-redux';

/**
 * Custom React Hook to get count value from state.
 * @see https://reactjs.org/docs/hooks-custom.html
 */
const useIsLoggedIn = () => useSelector(state => state.login.isLoggedIn);
const  getToken = ()=>useSelector(state=>state.login.access_token);
const getUserLang=()=>useSelector(state=>state.login.lang);
const getFrontLang=()=>useSelector(state=>state.login.frontLang);
const getIsSuperuser=()=>useSelector(state=>state.login.isSuperuser)
const getIsCountryManager=()=>useSelector(state=>state.login.isCountryManager)
const getIsMaManager=()=>useSelector(state=>state.login.isMaManager)

export  {useIsLoggedIn, getToken, getUserLang, getFrontLang, getIsSuperuser, getIsCountryManager,getIsMaManager};
