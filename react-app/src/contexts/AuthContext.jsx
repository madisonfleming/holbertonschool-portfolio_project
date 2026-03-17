//this file create e global context and every component can have access using useAuth the hook
import React, { useState, useEffect, useContext } from "react";
import { auth } from "../firebase/firebase";
import { onAuthStateChanged } from "firebase/auth";

//create a new context object with defalt value null
const AuthContext = React.createContext();

//a hook
export function useAuth() {
  return useContext(AuthContext);
}

//auth provider provides the auth to all the children(are the components which provider wraps)
export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  //tell us if user is log in or not
  const [userLoggedIn, setUserLoggedIn] = useState(false);
  //const [isEmailUser, setIsEmailUser] = useState(false);
  // const [isGoogleUser, setIsGoogleUser] = useState(false);
  //load the current state of the user
  const [loading, setLoading] = useState(true);

  //Token from BE, this endpoint was on dashboard now is here
  const [backendUser, setBackendUser] = useState(null);

  //use useEffect to subscribe to auth providers like firebase, login logout users, if login then go to initialize User
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, initializeUser);
    return unsubscribe;
  }, []);
  console.log("AuthProvider currentUser:", currentUser);
  console.log("AuthProvider backend user:", backendUser);
  async function initializeUser(user) {
    console.log("initialized user with ", user);
    try {
      if (!user) {
        //firebase return an obj so we can access to the token
        setCurrentUser(null);
        setUserLoggedIn(false);
        setBackendUser(null);
        return setLoading(false);
      }
      //clean BE user data
      setBackendUser(null);
      setCurrentUser(user);
      setUserLoggedIn(true);

      //validate token with backend
      await validateUser(user);
    } catch (error) {
      console.error("Error in initializeUser:", error);
    } finally {
      setLoading(false);
    }
  }

  //endpoint /protected from dashboard moved here
  async function validateUser(user) {
    try {
      const token = await user.getIdToken();
      console.log("TOKEN VALIDATE USER:", await user.getIdToken());
      //need to do fetch to an endpoint that use that function
      const response = await fetch("http://127.0.0.1:8000/api/users/me", {
        //firebase do the login -> generate the JWT
        //On HBNB was a POST because the login was manage by the back end but in here the login is manage by firebase so is GET the BE just return data
        headers: {
          //sending the token to the backend so fastapi receive it as a credential
          Authorization: `Bearer ${token}`,
        },
      });
      //geting the decoded token from the backend
      const data = await response.json();
      console.log("Backend validated user from /protected:", data);

      setBackendUser(data); // opcional
    } catch (error) {
      console.error("Error validating user:", error);
    }
  }
  //adding properties to the value object
  const value = {
    userLoggedIn,
    currentUser,
    backendUser,
    loading,
  };

  return (
    //children will have access to the value properties
    <AuthContext.Provider value={value}>
      {loading ? <h1 style={{ color: "red" }}>LOADING...</h1> : children}
    </AuthContext.Provider>
  );
}
