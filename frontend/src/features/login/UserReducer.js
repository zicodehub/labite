import * as constants from 'components/constants' ;
import * as type from './actionTypes';

const initialState = {
    access_token: undefined,
    isLoggedIn: false,
    logInError: false,
    email: undefined,
    lang: undefined,
    frontLang: constants.LANG.ENG.code,
    isSuperuser: false,
    isCountryManager: false,
    isMaManager: false,
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case `LOGIN`:
      return {
        ...state,
        access_token:action.payload.access_token,
        isLoggedIn:true,
        email: action.payload.email,
        lang: action.payload.lang,
        isSuperuser: action.payload.is_superuser,
        isCountryManager: action.payload.is_country_manager,
        isMaManager: action.payload.is_mas_admin,
      };

      case type.FRONT_LANG:
        return {
          ...state,
          frontLang: action.payload.frontLang
        };      

    case `LOGOUT`:
      return {
        ...state,
        access_token:undefined,
        isLoggedIn:false,
        email: undefined,
        lang:undefined,
        isSuperuser: false,
        isCountryManager: false,
        isMaManager: false
      };
    default:
      return state;
  }
};

export default reducer;
