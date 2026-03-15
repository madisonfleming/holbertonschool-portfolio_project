import "./MilestonesChild.css";
import ExportButton from "./ExportButton";
import { useEffect, useState } from "react";
import { useMilestones } from "../../contexts/MilestonesContext";

const MilestonesChild = ({
  current_num_of_books,
  target,
  selectedChild,
  certificateData,
  completedMilestones,
}) => {
  const percentage = Math.min((current_num_of_books / 1000) * 100, 100);

  return (
    <div className="milestoneChild-card">
      <h1 className="card-title"> Reading Progress </h1>
      <p className="card-subtitle"> {selectedChild.name} is doing great!</p>

      <div className="progress-hero">
        <div className="progress-percent">{Math.round(percentage)}%</div>
        <div className="progress-desc">
          of <strong>{selectedChild.name}</strong> target achieved!
        </div>
      </div>

      <div className="body-text">
        <div className="percentage">{Math.round(percentage)}%</div>
        of {selectedChild?.name}'s target achieved! That's{" "}
        {current_num_of_books} of {target} books!
      </div>
      <div className="export-btn">
        <ExportButton
          certificateData={certificateData}
          selectedChild={selectedChild}
        />
      </div>
    </div>
  );
};

export default MilestonesChild;
