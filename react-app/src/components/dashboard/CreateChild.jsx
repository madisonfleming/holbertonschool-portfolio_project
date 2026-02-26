import "./CreateChild.css";
import React from "react";

import { useState, useEffect } from "react";

const CreateChild = ({ trigger, setTrigger, createChild }) => {

  
  const [childName, setChildName] = useState("");
  const [date, setDate] = useState("");
  const [selectedAvatar, setSelectedAvatar] = useState(0);

  const avatars = [
  "/avatars/mlb-avatar-apple.png",
  "/avatars/mlb-avatar-bee.png",
  "/avatars/mlb-avatar-robot.png",
  "/avatars/mlb-avatar-sun.png"
  ];

  //we need a handle in order to create the obj with the states
    const handleCreateChild = () => {
      createChild({
        name: childName,
        date_of_birth: date,
        avatar_url: avatars[selectedAvatar],
      });

      setTrigger(false); // close popup
    };

  //handle to reset the data once we close the card
  const handleCloseResetData = () => {
    setChildName("");
    setDate("");
    setSelectedAvatar(0);
    setTrigger(false); // close popup
  }

  //use trigger to pop up the card if trigger then popup 
  return trigger ? (
    <div className="popup-overlay">
      <div className="CreateChildCard">
        {/* Close btn */}
        <button
            className="btn-close"
            onClick={handleCloseResetData}
          >✕
          </button>
          {/* create child */}
        <h1>Create a Child Profile</h1>
         <div className="create-child-layout">
           <div className="left-section">
              <h4>ABOUT</h4>
              {/* NAME */}
              <input type="text" 
              className="select-field-create-child" 
              placeholder="First Name"
              value={childName}
              onChange={(e) => setChildName(e.target.value)}
              />
              {/* DOB */}
              <input
                    type="date"
                    className="select-field-create-child"
                    id="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                  />
            </div>
            {/* Avatar section */}
          <div className="avatar-section">
            <h4>PICK AVATAR</h4>
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
          <button className="btn-submit"onClick={handleCreateChild}>Create Profile</button>
        </div>
      </div>
    </div>
  ) : (
    ""
  );
};

export default CreateChild;
