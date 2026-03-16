import { useEffect, useState } from "react";
import { useAuth } from "../../contexts/AuthContext";
import WeeklyGoal from "../../components/dashboard/WeeklyGoal";
import { getWeeklyTheme } from "../../utils/GetWeeklyTheme";
import "./dashboard.css";
import AddReadingSession from "../../components/dashboard/AddReadingSession";
import { useChild } from "../../contexts/ChildContext";
import ChildCard from "../../components/dashboard/ChildCard";

// dashboard only loads popups cards show components NOT LOGIC ON BE thats context
const Dashboard = () => {
  //we use context to import useChild
  const { childList, selectedChild } = useChild();
  const { currentUser } = useAuth();
  const theme = getWeeklyTheme();
  const [buttonAddReadingSessionPopup, setButtonAddReadingSessionPopup] =
    useState(false);

  const target = 5; //hardcoded to send to BE once is finished

  return (
    <div>
      <div className="reading-session-container">
        <img
          src={`open-book.png`}
          className="open-book-img"
          onClick={() => setButtonAddReadingSessionPopup(true)}
          type="button"
        />
        <p className="reading-text">Add Reading Session</p>
      </div>
      <h1 className="dashboard-title">Let's get reading, wormies!</h1>
      <AddReadingSession
        trigger={buttonAddReadingSessionPopup}
        setTrigger={setButtonAddReadingSessionPopup}
        children_RS={childList}
      ></AddReadingSession>
      <div className="dashboard-grid">
        <div className="children-container">
          <ChildCard />
        </div>
        <div className="weekly-container">
          <WeeklyGoal target={target} theme={theme} />
        </div>
        {/* 
        <div className="milestones-container">
          <Milestones current_num_of_books={current_num_of_books} target={target} />
        </div>
        */}
      </div>
    </div>
  );
};

export default Dashboard;
