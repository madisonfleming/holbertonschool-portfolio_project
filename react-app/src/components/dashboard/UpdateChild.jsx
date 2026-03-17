import "./UpdateChild.css";
import React from "react";
import toast from "react-hot-toast"; // for user facing alerts/error messages

import { useState, useEffect } from "react";

const UpdateChild = ({ child, trigger, setTrigger, updateChild }) => {
  //this take the states that receive as a prop (child) so when the pop up opne it fills with child info
  const [childName, setChildName] = useState(child?.name || "");
  const [date, setDate] = useState(child?.date_of_birth || "");
  const [selectedAvatar, setSelectedAvatar] = useState(child?.avatar || 0);

  const avatars = [
    "/avatars/mlb-avatar-apple",
    "/avatars/mlb-avatar-bee",
    "/avatars/mlb-avatar-robot",
    "/avatars/mlb-avatar-sun",
  ];
  // Sync state when child changes
  useEffect(() => {
    if (child) {
      setChildName(child.name || "");
      setDate(child.date_of_birth || "");
      setSelectedAvatar(child.avatar || 0);
    }
  }, [child]);

  //we need a handle in order to create the obj with the states
  //we send name, date_of_birth and avatar_url but in react FE we call childName date and avatars
  const handleUpdateChild = async () => {
    //if the user doesnt put a new avatar the last avatar is saved
    //name: childName,
    //date_of_birth: date,
    //avatar_url: avatars[selectedAvatar],
    // # && # !==  -> if # is valid and is dif from original then:
    const updatedData = {};

    if (childName && childName !== child.name) {
      updatedData.name = childName;
    }
    if (date && date !== child.date_of_birth) {
      updatedData.date_of_birth = date;
    }
    if (avatars[selectedAvatar] !== child.avatar) {
      updatedData.avatar_url = avatars[selectedAvatar];
    }
    console.log("sending update data for test: ", updatedData);
    try {
      await updateChild(child.id, updatedData);
      setTrigger(false); // close popup
      toast.success("Child updated successfully."); // custom success message
    } catch(error) {
      toast.error(error.message); // custom error message (error msg received from contexts depending on status code)
    }};

  //handle to reset the data once we close the card
  const handleCloseResetData = () => {
    setChildName("");
    setDate("");
    setSelectedAvatar(0);
    setTrigger(false); // close popup
  };

  //use trigger to pop up the card if trigger then popup
  return trigger ? (
    <div className="popup-overlay">
      <div className="UpdateChildCard">
        {/* Close btn */}
        <button className="btn-close" onClick={handleCloseResetData}>
          ✕
        </button>
        {/* update child */}
        <h1 className="tittle-popup-card">
          Update {child?.name || "Child"} Profile
        </h1>
        <div className="update-child-layout">
          <div className="left-section">
            <h4 className="subtittle-popup-card">Update Personal Info</h4>
            {/* NAME */}
            <input
              type="text"
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
            <h4 className="subtittle-popup-card">
              Relationship with {child?.name || "Child"}
            </h4>
            <input
              type="text"
              className="select-field-update-child"
              placeholder="Who are you?"
            />
          </div>
          {/* Avatar section */}
          <div className="avatar-section">
            <h4 className="subtittle-popup-card">Pick New Avatar</h4>
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
          <button className="btn-submit" onClick={handleUpdateChild}>
            Update Child
          </button>
        </div>
      </div>
    </div>
  ) : (
    ""
  );
};

export default UpdateChild;
