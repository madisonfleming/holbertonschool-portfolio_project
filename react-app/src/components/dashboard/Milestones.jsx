
import { useChild } from '../../contexts/ChildContext'
import "./Milestones.css"
const Milestones = ({ current_num_of_books, target, selectedChild, certificateData }) => {
  const percentage = Math.min((current_num_of_books / 1000) * 100, 100);
 



  return (
    <div className="milestone-card">
      <div>
      <h2>Milestones</h2>
      <button>
        History
      </button>
      
      </div>
      <p className="header-text">
        <p className="name">
          {selectedChild.name}
          </p>
          <p className="milestone-text">is doing great!</p>
        {Math.round(percentage)}% of {selectedChild?.name}'s target achieved! That's {current_num_of_books} of {target} books!
      </p>

    </div>
  )

}

export default Milestones
