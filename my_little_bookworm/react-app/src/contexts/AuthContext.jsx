//this file create e global context and every component can have access using useAuth the hook
import React, {useState, useEffect, useContext} from "react";
import { auth } from "../firebase/firebase";
import { onAuthStateChanged } from "firebase/auth";

//create a new context object with defalt value null
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
