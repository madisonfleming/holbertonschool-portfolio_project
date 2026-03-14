import { useChild } from "../../contexts/ChildContext";
import "./MilestonesHistory.css";
import ExportButton from "./ExportButton";
import CompletedMilestones from "./CompletedMilestones";
import { ClipPath } from "@react-pdf/renderer";
import { useEffect, useState } from "react";
import { useMilestones } from "../../contexts/MilestonesContext";

const MilestonesHistory = ({ selectedChild }) => {
  //We need to save the milestones in states
  /* 1. Call endpoint inside useEffect. 
  2 Saved Milestones on useState 
  3.Render the state. 
  4 Send id of selectedChild */
  const { allMilestonesPerChild } = useMilestones();
  const { weeklyGoalMilestonesPerChild } = useMilestones();
  const { booksReadMilestonesPerChild } = useMilestones();
  const [milestonesPerChild, setMilestonesPerChild] = useState([]);
  const [getWeeklyGoalMilestonesPerChild, setWeeklyGoalMilestonesPerChild] =
    useState([]);
  const [getBooksReadMilestonesPerChild, setBooksReadMilestonesPerChild] =
    useState([]);

  const icons = {
    books: '<img src="/open-book.png" />',
    weekly: '<img src="/open-book.png" />',
  };
  const labels = { books: "Books Milestone", weekly: " Weekly Goal" };

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
    }

    fetchDataFromMilestonesPerChild();
  }, [selectedChild]);

  return (
    <div className="milestoneHistory-card">
      <h1 className="card-title"> Milestones </h1>
      <p className="card-subtitle"> {selectedChild.name}'s achievements</p>
      {/* Filter tabs*/}
      <div className="filter-row">
        <button
          className="filter-tab active"
          onclick="filterMilestones('books', this)"
        >
          Books Read
        </button>
        <button class="filter-tab" onclick="filterMilestones('weekly', this)">
          Weekly Goal
        </button>
      </div>

      {/*Timeline*/}
      <div class="timeline-wrap">
        <div class="timeline" id="timeline"></div>
        <div class="empty-state" id="emptyState">
          <div class="empty-text">No milestones yet!</div>
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
