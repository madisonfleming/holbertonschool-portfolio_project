import "./MilestonesHistory.css";
import { useEffect, useState } from "react";
import { useMilestones } from "../../contexts/MilestonesContext";

const MilestonesHistory = ({ selectedChild }) => {
  //We need to save the milestones in states
  /* 1. Call endpoint inside useEffect. 
  2 Saved Milestones on useState 
  3.Render the state. 
  4 Send id of selectedChild */
  const { allMilestonesPerChild } = useMilestones();
  // const { weeklyGoalMilestonesPerChild } = useMilestones();
  // const { booksReadMilestonesPerChild } = useMilestones();
  const [milestonesPerChild, setMilestonesPerChild] = useState([]);
  //const [getWeeklyGoalMilestonesPerChild, setWeeklyGoalMilestonesPerChild] =  useState([]);
  //const [getBooksReadMilestonesPerChild, setBooksReadMilestonesPerChild] = useState([]);

  const icons = {
    books_read: "/mlb-star.png",
    weekly_goal: "/mlb-trophy.png",
  };
  const labels = { books_read: "Books", weekly_goal: " Weekly" };

  const [filter, setFilter] = useState("books_read");

  const filtered = milestonesPerChild.filter((data) => data.type === filter);

  useEffect(() => {
    if (!selectedChild?.id) return;

    //this fetch is to see the milestons per child
    async function fetchDataFromMilestonesPerChild() {
      //all milestones
      const dataAllMilestones = await allMilestonesPerChild(selectedChild.id);
      console.log(
        "DataAllMilestones FROM BE ON SELECTED CHILD INSIDE MilestonesHistoryjsx:",
        dataAllMilestones,
      );
      setMilestonesPerChild(dataAllMilestones);
      /*
      //just weekly goal
      const dataWeeklyGoalMilestones = await weeklyGoalMilestonesPerChild(
        selectedChild.id,
      );
      console.log(
        "Dataweeklygoalmilestones FROM BE ON SELECTED CHILD INSIDE MilestonesHistoryjsx:",
        dataWeeklyGoalMilestones,
      );
      setWeeklyGoalMilestonesPerChild(dataWeeklyGoalMilestones);
      //just books read
      const dataBooksReadMilestones = await booksReadMilestonesPerChild(
        selectedChild.id,
      );
      console.log(
        "DataReadBooksMilestones FROM BE ON SELECTED CHILD INSIDE MilestonesHistoryjsx:",
        dataBooksReadMilestones,
      );
      setBooksReadMilestonesPerChild(dataBooksReadMilestones);
      */
    }

    fetchDataFromMilestonesPerChild();
  }, [selectedChild]);

  //small function for date
  function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      day: "numeric",
      month: "long",
      year: "numeric",
    });
  }

  return (
    <div className="milestoneHistory-card">
      <h1 className="card-title"> Milestones </h1>
      <p className="card-subtitle"> {selectedChild?.name} achievements</p>
      {/* Filter tabs */}
      <div className="filter-row">
        <button
          className={`filter-tab ${filter === "books_read" ? "active" : ""}`}
          onClick={() => setFilter("books_read")}
        >
          Books Read
        </button>
        <button
          className={`filter-tab ${filter === "weekly_goal" ? "active" : ""}`}
          onClick={() => setFilter("weekly_goal")}
        >
          Weekly Goal
        </button>
      </div>

      {/* Timeline with box description */}
      <div className="timeline-wrap">
        {/* This style: animationDelay is for every item appear 0.05 seconds after */}
        <div className={`timeline ${filtered.length === 0 ? "empty" : ""}`}>
          {filtered.length === 0 ? (
            <>
              <div className="empty-text">No milestones yet! </div>
              <div className="empty-text-strong">
                Start your journey by adding a reading session or complete a
                weekly goal!{" "}
              </div>
            </>
          ) : (
            filtered.map((dataFromBEMilestones, index) => (
              <div
                key={index}
                className="milestone-item"
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <div className={`milestone-icon ${dataFromBEMilestones.type}`}>
                  <img
                    src={icons[dataFromBEMilestones.type]}
                    alt={dataFromBEMilestones.type}
                  />
                </div>
                <div className="milestone-content">
                  <div
                    className={`milestone-type ${dataFromBEMilestones.type}`}
                  >
                    {labels[dataFromBEMilestones.type]}
                  </div>
                  <div className="milestone-text">
                    {dataFromBEMilestones.description}
                  </div>
                  <div className="milestone-date">
                    {formatDate(dataFromBEMilestones.completed_at)}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
      {/* 
      <div className="milestone-badges">
        {milestonesPerChild.length === 0 ? (
          <p>No milestones yet</p>
        ) : (
          milestonesPerChild.map((data) => (
            <div key={data.id}>
              <strong>{data.description}</strong>
            </div>
          ))
        )}

        {getWeeklyGoalMilestonesPerChild.length === 0 ? (
          <p>No milestones yet</p>
        ) : (
          getWeeklyGoalMilestonesPerChild.map((data) => (
            <div key={data.id}>
              <strong>{data.description}</strong>
            </div>
          ))
        )}

        {getBooksReadMilestonesPerChild.length === 0 ? (
          <p>No milestones yet</p>
        ) : (
          getBooksReadMilestonesPerChild.map((data) => (
            <div key={data.id}>
              <strong>{data.description}</strong>
            </div>
          ))
        )}
      </div>
      */}
    </div>
  );
};
export default MilestonesHistory;
