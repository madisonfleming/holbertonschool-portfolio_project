import "./CreateChild.css";
import React from "react";

import { useState, useEffect } from "react";

const CreateChild = ({ trigger, setTrigger }) => {
  const [childName, setChildName] = useState("");
  const [date, setDate] = useState("");
  const [selectedAvatar, setSelectedAvatar] = useState(0);

  const avatars = [
  "/avatars/mlb-avatar-apple.png",
  "/avatars/mlb-avatar-bee.png",
  "/avatars/mlb-avatar-robot.png",
  "/avatars/mlb-avatar-sun.png"
];


  return trigger ? (
    <div className="popup-overlay">
      <div className="CreateChildCard">
        <h1>Create a Child Profile</h1>
         <div className="create-child-layout">
           <div className="left-section">
              <h4>ABOUT</h4>
              <input type="text" 
              className="select-field-create-child" 
              placeholder="First Name"
              value={childName}
              onChange={(e) => setChildName(e.target.value)}
              />
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
        <div className="button-section">
          <button
            className=" btn btn-close-submit"
            onClick={() => setTrigger(false)}
          >
            Close
          </button>
          <button className="btn btn-close-submit">Create Profile</button>
        </div>
      </div>
    </div>
  ) : (
    ""
  );
};

export default CreateChild;
