
import "./Milestones.css"
const Milestones = ({ current_num_of_books, target }) => {
  const percentage = Math.min((current_num_of_books / 1000) * 100, 100);

  return (
    <div className="worm-card">
      <h2>Milestone Progress</h2>
      <div className="worm-container">
        <div className="worm-fill" style={{ width: `${percentage}%` }}
        ></div>
      </div>
      <p className="worm-text">
        {Math.round(percentage)}% — {current_num_of_books} of {target} books.
      </p>
    </div>
  )

}

export default Milestones