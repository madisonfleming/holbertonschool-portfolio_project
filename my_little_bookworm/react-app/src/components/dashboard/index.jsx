import React from 'react'
import { useAuth } from '../../contexts/AuthContext'

const Dashboard = () => {
    const { currentUser } = useAuth();
    
    const getToken = async () => {
    const token = await currentUser.getIdToken();
    console.log("Token:", token);
  };

    return (
        
        <div>
        <button onClick={getToken}>
            Obtener token
        </button>
        Hello {currentUser.displayName ? currentUser.displayName : currentUser.email}, you are now logged in Dashboard.
        </div>
    )
}         

export default Dashboard