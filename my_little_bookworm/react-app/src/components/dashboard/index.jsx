import { useEffect } from "react";
import { useAuth } from '../../contexts/AuthContext'
import { ProfileSwitcher } from "./childProfile";
import axios from "axios";
import { Header } from "../header";

const Dashboard = () => {
    const { currentUser } = useAuth();

    //
    async function loadData() {
    if (!currentUser) return;

    try {
      const token = await currentUser.getIdToken();
      const response = await axios.get(
        "http://127.0.0.1:8000/api/v1/protected", 
        {
          headers: {
            "Authorization": `Bearer ${token}`,
      },
    }
    );

    console.log("Backend response:", response.data);
    } catch (error) {
      console.error("Error calling backend:", error);
    }

  };
  //to validate the existance of user useEffect detecs the change of currentUser from null to login
   useEffect(() => {
    loadData();
  }, [currentUser]);

    return (
        <><div className="dashboard">
        <Header />
      </div>
      <div>
          Hello {currentUser.displayName ? currentUser.displayName : currentUser.email}, you are now logged in Dashboard.
        </div>
        <ProfileSwitcher />
        </>
    );
}; 

export default Dashboard

