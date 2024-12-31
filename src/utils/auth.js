
export const setAuthToken = (token) => {
    if (token) {
      localStorage.setItem('authToken', token);
    } else {
      localStorage.removeItem('authToken');
    }
  };
  
  export const getAuthToken = () => {
    return localStorage.getItem('authToken');
  };
  