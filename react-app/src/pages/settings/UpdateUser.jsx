import "./UpdateUser.css";
import React from "react";

import { useState, useEffect } from "react";

const UpdateUser = ({ user, trigger, setTrigger, updateUser }) => {

  const [userName, setUserName] = useState(user?.name || "");
  const [email, setEmail] = useState(user?.email || "");
  const [password, setPassword] = useState(user?.password || "");

   // Sync state when user changes
  useEffect(() => {
    if (user) {
      setUserName(user.name || "");
      setEmail(user.email || "");
      setPassword(user.password || "");
    }
  }, [user]);

  //we need a handle in order to create the obj with the states
    const handleUpdateUser = () => {
      const updatedData = {
        name: userName,
        email: email,
        password: password,
      };

      console.log("sending update data for test: ", updatedData);
      updateUser(user.id, updatedData);

      setTrigger(false); // close popup
    };

  //handle to reset the data once we close the card
  const handleCloseResetData = () => {
    setUserName("");
    setEmail("");
    setPassword("");
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
          {/* update child */}
        <h1 className="tittle-popup-card">Update {child?.name || "Child"} Profile</h1>
         <div className="update-child-layout">
           <div className="left-section">
              <h4 className= "subtittle-popup-card">About</h4>
              {/* NAME */}
              <input type="text" 
              className="select-field-update-child" 
              placeholder="First Name"
              value={childName}
              onChange={(e) => setChildName(e.target.value)}
              />
              {/* DOB */}
              <input
                    type="date"
                    className="select-field-update-child"
                    id="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                  />
              {/* Relationship JUST MOCKED RIGHT NOW */}
              <h4 className= "subtittle-popup-card">Relationship with {child?.name || "Child"}</h4>
              <input type="text" 
              className="select-field-update-child" 
              placeholder="Who are you?"
              />
            </div>
            {/* Avatar section */}
          <div className="avatar-section">
            <h4 className= "subtittle-popup-card">Pick New Avatar</h4>
            <div className="avatar-list">
              {avatars.map((avatar, index) => (
                <div
                  key={index}
                  className={`avatar-option ${selectedAvatar === index ? "selected" : ""}`}
                  onClick={() => setSelectedAvatar(index)}
                >
                  <img src={avatar} className="avatar-img" />
                </div>
              ))}
            </div>
          </div>
        </div>
        {/* SUBMIT BTN */}
        <div className="button-section">
          <button className="btn-submit"onClick={handleUpdateChild}>Update Child</button>
        </div>
      </div>
    </div>
  ) : (
    ""
  );
};

export default UpdateChild;
