import { useEffect } from "react";
import { useAuth } from '../../contexts/AuthContext'

const Dashboard = () => {
  const { currentUser } = useAuth();

  //
  async function loadData() {
    if (!currentUser) return;

    const token = await currentUser.getIdToken();
    console.log("Token:", token);
    //need to do fetch to an endpoint that use that function
    const response = await fetch("http://127.0.0.1:8000/api/protected", {
      //firebase do the login -> generate the JWT
      //On HBNB was a POST because the login was manage by the back end but in here the login is manage by firebase so is GET the BE just return data
      headers: {
        //sending the token to the backend so fastapi receive it as a credential
        "Authorization": `Bearer ${token}`
      }
    });
    //geting the decoded token from the backend
    const data = await response.json();
    console.log("this is data:", data);
  };
  //to validate the existance of user useEffect detecs the change of currentUser from null to login
  useEffect(() => {
    loadData();
  }, [currentUser]);

  return (

    <div>
      Hello {currentUser.displayName ? currentUser.displayName : currentUser.email}, you are now logged in Dashboard.
    </div>
  )
}

export default Dashboard

