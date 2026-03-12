
import { useChild } from '../../contexts/ChildContext'
import "./MilestonesHistory.css"
import ExportButton from './ExportButton';
import CompletedMilestones from './CompletedMilestones';
import { ClipPath } from '@react-pdf/renderer';
import { useEffect, useState } from "react";
import { useMilestones } from "../../contexts/MilestonesContext";


const MilestonesHistory = ({ selectedChild }) => {
  //We need to save the milestones in states
  /* 1. Call endpoint inside useEffect. 
  2 Saved Milestones on useState 
  3.Render the state. 
  4 Send id of selectedChild */ 
  const { allMilestonesPerChild } = useMilestones();
  const [milestonesPerChild, setMilestonesPerChild] = useState([]);

  useEffect(() => {
    if (!selectedChild?.id) return;

    async function fetchDataFromAllMilestonesPerChild() {
      const data = await allMilestonesPerChild(selectedChild.id);
      console.log("DATA FROM BE ON SELECTED CHILD INSIDE MilestonesHistoryjsx:", data);
      setMilestonesPerChild(data); 
    }

    fetchDataFromAllMilestonesPerChild();
  }, [selectedChild]);

  return (
  <div className="milestoneHistory-card">
    <h2>Milestones History</h2>
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

      </div>
  </div>
  )

}
export default MilestonesHistory
