import "./settings.css"
import { useState, useEffect } from "react";
import { useAuth } from "../../contexts/AuthContext";
import CreateChild from "../../components/dashboard/CreateChild";
import { useChild } from "../../contexts/ChildContext";
import ChildCardSettings from "../../components/settings/ChildCardSettings"; 



const Settings = () => {
    const [user, setUser] = useState([]);
    const [loading, setLoading] = useState(true);
    const { currentUser } = useAuth();
    //we use context to import useChild
    const { childList, createChild, updateChild } = useChild();
    const [buttonCreateChildPopup, setButtonCreateChildPopup] = useState(false);
   

    
    async function loadData() {
        //GET USER DATA
        if (!currentUser) return;
        try {
            const token = await currentUser.getIdToken();
            // fetching /users endpoints
            const response = await fetch("http://127.0.0.1:8000/api/users/me", {
                headers: {
                    //sending the token to the backend so fastapi receive it as a credential
                    Authorization: `Bearer ${token}`,
                },
            });
            //geting user from the backend
            const users = await response.json();
            console.log("this is user data", users);

            //incase we do the relationships and map multiple users. thought this would b handy
            //const formatted = users.map((user) => ({
            //    id: user.id,
            //    name: user.name,
            //    email: user.email,
            //}));
            setUser(users);
            setLoading(false)

        } catch (error) {
            console.error("Error fetch user", error)
        }


    }
    //UPDATE USER
    async function updateUser(id, updatedData) {
        console.log("PUT data:", updatedData);

        if (!currentUser) return;

        const token = await currentUser.getIdToken();

        const response = await fetch(`http://127.0.0.1:8000/api/users/me/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(updatedData),
        });

        if (!response.ok) {
            console.error("Error updating user");
            return;
        }

        const updatedUser = await response.json();
        console.log("Answer from BE of updating a user:", updatedUser);
        // Update local state

        setUserList(prev => {
            const updatedList = prev.map(user => {
                if (user.id === id) {
                    // search the user we want to update
                    return {
                        ...user,
                        ...updatedUser,
                    };
                } else {
                    // if new data is not send stay with the old data
                    return user;
                }
            });

            return updatedList;
        });

    }

    //to validate the existance of user useEffect detecs the change of currentUser
    useEffect(() => {
        loadData();
    }, [currentUser]);


    return (
        <div className="settings-container">
            <div className="settings-card">
                <h1 className="title">Hello, {user.name}</h1>
                <p className="subtitle">Account Details</p>
                <form >
                    <p className="username">{user.name}</p>
                    <p className="username">{user.email}</p>
                    <button className="edit-btn">Edit Account</button>
                </form>
            </div>
            <div className="settings-child-card">
                <h1 className="title">Your Children!</h1>
                <ChildCardSettings
                    childrenList={childList}
                    />

            <div className="divider"> </div>
            {/* createChild buttom for testing*/}
            <button className="btn-submit-create"
              onClick={() => setButtonCreateChildPopup(true)}
            >Create Child
            </button>
          {/* For pop up the create child card  need to be outside so the weekly goal text doesnt appear infront */}
          {/*FE send to the BE a POST with this json */}
          <CreateChild
            trigger={buttonCreateChildPopup}
            setTrigger={setButtonCreateChildPopup}
            createChild={createChild}
          ></CreateChild>
            </div>
        </div>
    );
}

export default Settings;
