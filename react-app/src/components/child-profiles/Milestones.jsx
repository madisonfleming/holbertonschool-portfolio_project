
import { useChild } from '../../contexts/ChildContext'
import "./Milestones.css"
import ExportButton from './ExportButton';
import CompletedMilestones from './CompletedMilestones';
import { ClipPath } from '@react-pdf/renderer';

const Milestones = ({ current_num_of_books, target, selectedChild, certificateData, completedMilestones }) => {
  const percentage = Math.min((current_num_of_books / 1000) * 100, 100);


  return (
    <div className="milestone-card">
      <div className="left-side">
        <p className="milestone-text">{selectedChild.name} is doing great!</p>
          <div className="body-text">
            <div className="percentage">{Math.round(percentage)}%</div>
             of {selectedChild?.name}'s target achieved! That's {current_num_of_books} of {target} books!
          </div>
          <div className="export-btn">
            <ExportButton certificateData={certificateData} selectedChild={selectedChild}/>
          </div>
    </div>
    <div className="right-side">
        <h2>Milestones</h2>
      <h3>History</h3>
      <div className="milestone-badges">
        <CompletedMilestones completedMilestones={completedMilestones}/>
      </div>
    </div>

    </div>
  )

}

export default Milestones
