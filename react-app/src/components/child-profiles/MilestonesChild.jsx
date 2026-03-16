import "./MilestonesChild.css";
import ExportButton from "./ExportButton";
import { useEffect, useState } from "react";
import { useBooks } from "../../contexts/BooksContext";
import { data } from "react-router-dom";

const MilestonesChild = ({ selectedChild, certificateData }) => {
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

  return (
    <div className="milestoneChild-card">
      <h1 className="card-title"> Reading Progress </h1>
      <p className="card-subtitle"> {selectedChild.name} is doing great!</p>

      <div className="progress-hero">
        <div className="progress-percent">{Math.round(percentage)}%</div>
        <div className="progress-desc">
          of <strong>{selectedChild.name} </strong>
          target achieved!
        </div>
      </div>

      <div className="stats-row">
        <div className="stat-box">
          <span className="stat-value">100</span>
          <span className="stat-label">Read</span>
        </div>
        <div className="stat-box">
          <span className="stat-value">900</span>
          <span className="stat-label">To go</span>
        </div>
        <div className="stat-box">
          <span className="stat-value">10%</span>
          <span className="stat-label">Done</span>
        </div>
      </div>

      <div className="divider"></div>
      <div className="btn-row">
        <button className="btn-mc"> Preview Reward</button>
        <button className="btn-mc"> Download Reward</button>
        {/*<ExportButton
          certificateData={certificateData}
          selectedChild={selectedChild}
        />*/}
      </div>
    </div>
  );
};

export default MilestonesChild;
