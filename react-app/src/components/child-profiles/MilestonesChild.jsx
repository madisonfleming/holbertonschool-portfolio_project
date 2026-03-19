import "./MilestonesChild.css";
import ExportButton from "./ExportButton";
import { useEffect, useState } from "react";
import { useBooks } from "../../contexts/BooksContext";
import { data } from "react-router-dom";
import GetWorm from "../dashboard/GetWorm";
import { useMilestones } from "../../contexts/MilestonesContext";

const MilestonesChild = ({ selectedChild }) => {
  if (!selectedChild) return "No child selected";
  const { getReadingSessionsCount } = useBooks();
  const [count, setCount] = useState(0);

  useEffect(() => {
    async function loadCount() {
      const count_from_endpoint = await getReadingSessionsCount();
      setCount(count_from_endpoint);
    }

    loadCount();
  }, [selectedChild]);
  const percentage = Math.min((count / 1000) * 100, 100);
  const rest = Math.max(1000 - count, 0);

  //GET SINGLE MILESTONE DATA FROM getSingleMilestone endpoint
  const { getSingleMilestone } = useMilestones();
  const [data, setData] = useState();

  useEffect(() => {
    async function loadMilestone() {
      const certificateData = await getSingleMilestone(selectedChild.id);
      setData(certificateData);
    }
    loadMilestone();
  }, [selectedChild]);

  console.log("data being sent from milestoneChild", data);

  return (
    <div className="milestoneChild-card">
      <h1 className="card-title"> Reading Progress </h1>
      <p className="card-subtitle"> {selectedChild.name} is doing great!</p>
      <div className="worm">
        <GetWorm selectedChild={selectedChild} />
      </div>

      <div className="progress-hero">
        <div className="progress-percent">{Math.floor(percentage)}%</div>
        <div className="progress-desc">
          of <strong> {selectedChild.name}'s </strong>
          target achieved!
        </div>
      </div>

      <div className="stats-row">
        <div className="stat-box">
          <span className="stat-value">{count}</span>
          <span className="stat-label">Read</span>
        </div>
        <div className="stat-box">
          <span className="stat-value">{rest}</span>
          <span className="stat-label">To go</span>
        </div>
        <div className="stat-box">
          <span className="stat-value">{Math.floor(percentage)}%</span>
          <span className="stat-label">Done</span>
        </div>
      </div>
      <div className="reward-section">
        <div className="reward-title">Your reward is ready!</div>
        <div className="reward-desc">Download your certificate</div>
        <div className="btn-row">
          {/* EXPORT BTN */}
          <ExportButton selectedChild={selectedChild} data={data} />
        </div>
      </div>
    </div>
  );
};

export default MilestonesChild;
