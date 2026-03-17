import "./CreateChild.css";
import React from "react";
import { useChild } from "../../contexts/ChildContext";
import { useState, useEffect } from "react";
import toast from "react-hot-toast"; // for user facing alerts/error messages

const CreateChild = ({ trigger, setTrigger, createChild }) => {
  const [childName, setChildName] = useState("");
  const [date, setDate] = useState("");
  const [selectedAvatar, setSelectedAvatar] = useState(0);

  const avatars = [
    "/avatars/mlb-avatar-apple",
    "/avatars/mlb-avatar-bee",
    "/avatars/mlb-avatar-robot",
    "/avatars/mlb-avatar-sun",
  ];

  //we need a handle in order to create the obj with the states
  // we need to POST in order to the BE to received name, date_of_birth, avatar_url
  const handleCreateChild = async () => {
    try {
      await createChild({
      name: childName,
      date_of_birth: date,
      avatar_url: avatars[selectedAvatar],
    });
    setTrigger(false); // close popup
    toast.success("Child created successfully."); //custom success msg for user
    } catch (error) {
      toast.error(error.message); // custom error msg (error msg received from contexts depending on status code)
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
      <div className="CreateChildCard">
        {/* Close btn */}
        <button className="btn-close" onClick={handleCloseResetData}>
          ✕
        </button>
        {/* create child */}
        <h1 className="tittle-popup-card">Create a Child Profile</h1>
        <div className="create-child-layout">
          <div className="left-section">
            <h4 className="subtittle-popup-card">About</h4>
            {/* NAME */}
            <input
              type="text"
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
            {/* Relationship JUST MOCKED RIGHT NOW */}
            <h4 className="subtittle-popup-card">
              Relationship with the Child
            </h4>
            <input
              type="text"
              className="select-field-create-child"
              placeholder="Who are you?"
            />
          </div>
          {/* Avatar section */}
          <div className="avatar-section">
            <h4 className="subtittle-popup-card">Pick Avatar</h4>
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
          <button className="btn-submit" onClick={handleCreateChild}>
            Create Profile
          </button>
        </div>
      </div>
    </div>
  ) : (
    ""
  );
};

export default CreateChild;
