//this file create e global context and every component can have access using useAuth the hook
import React, {useState, useEffect, useContext} from "react";
import { auth } from "../firebase/firebase";
import { onAuthStateChanged } from "firebase/auth";

//create a new context object with defalt value null
//Auth context es who know if user is authenticated so the endpoint for users go here
//here we create user if doesnt exist with the new claim 
const AuthContext = React.createContext()

//a hook
export function useAuth(){
  return useContext(AuthContext);
}

//auth provider provides the auth to all the children(are the components which provider wraps)
export function AuthProvider({ children }){
  const [currentUser, setCurrentUser] = useState(null);
  //tell us if user is log in or not
  const [userLoggedIn, setUserLoggedIn] = useState(false);
 //const [isEmailUser, setIsEmailUser] = useState(false);
 // const [isGoogleUser, setIsGoogleUser] = useState(false);
  //load the current state of the user
  const [loading, setLoading] = useState(true);

  //use useEffect to subscribe to auth providers like firebase, login logout users, if login then go to initialize User
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, initializeUser);
    return unsubscribe;
  }, []);

  async function initializeUser(user) {
    if (user) {
      //firebase return an obj so we can access to the token
      //Inside here firebase know that user is authnticated, so if user doesnt exist is created in the 
      //backend, assign custom claim, do the refresh token, save user and load dashboard
      
      // 1. We create the user is doesnt exist on the backend
      await fetch("http://127.0.0.1:8000/api/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          firebase_uid: user.uid,
          name: user.displayName,
          email: user.email,
        }),
      });

      // 2. Refresh the token to obtain the custom claim, here is wher ethe claim is added
      await user.getIdToken(true);
      // 3. Save user in the context
      setCurrentUser(user);
      setUserLoggedIn(true);
    } else {
      //user not login
      setCurrentUser(null);
      setUserLoggedIn(false);
    }

    setLoading(false);
  }


  //adding properties to the value object
 const value = {
    userLoggedIn,
    currentUser,
    loading
  };

  return(
    //children will have access to the value properties
    <AuthContext.Provider value={value}>
    {!loading && children}
    </AuthContext.Provider>
  )

}
