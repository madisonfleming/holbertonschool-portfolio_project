import "./UpdateUser.css";
import React from "react";

import { useState, useEffect } from "react";

const UpdateUser = ({ user, trigger, setTrigger, updateUser }) => {

  const [userName, setUserName] = useState(user?.name || "");
  const [email, setEmail] = useState(user?.email || "");
  //const [password, setPassword] = useState(user?.password || "");

   // Sync state when user changes
  useEffect(() => {
    if (user) {
      setUserName(user.name || "");
      setEmail(user.email || "");
      //setPassword(user.password || "");
    }
  }, [user]);

  //we need a handle in order to create the obj with the states
    const handleUpdateUser = () => {
      const updatedData = {
        name: userName,
        email: email,
        //password: password,
      };

      console.log("sending update data for test: ", updatedData);
      updateUser(updatedData);

      setTrigger(false); // close popup
    };

  //handle to reset the data once we close the card
  const handleCloseResetData = () => {
    setUserName("");
    setEmail("");
    //setPassword("");
    setTrigger(false); // close popup
  }

  //use trigger to pop up the card if trigger then popup 
  return trigger ? (
    <div className="popup-overlay">
      <div className="UpdateUser">
        {/* Close btn */}
        <button
            className="btn-close"
            onClick={handleCloseResetData}
          >✕
          </button>
          {/* update user */}
        <h1 className="update-popup-card">Update {user?.name || "User"} Profile</h1>
         <div className="update-user-layout">
              <h4 className= "subtitle-popup-card">Update Personal Info</h4>
              {/* NAME */}
              <input type="text" 
              className="select-field-update-child" 
              placeholder="Edit First Name"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              />
              {/* EMAIL */}
              <input
                    type="email"
                    className="select-field-update-child"
                    placeholder="Edit Email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
            </div>

        {/* SUBMIT BTN */}
        <div className="button-section">
          <button className="btn-submit"onClick={handleUpdateUser}>Submit</button>
        </div>
      </div>
    </div>
  ) : (
    ""
  );
};

export default UpdateUser;
