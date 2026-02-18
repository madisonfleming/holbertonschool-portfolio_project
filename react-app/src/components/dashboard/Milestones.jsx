

import "./Milestones.css"
const Milestones = ({ current_num_of_books, target }) => {
  const percentage = Math.min((current_num_of_books / 1000) * 100, 100);

  return (
    <div className="milestone-card">
      <h2>Milestone Progress</h2>
      <p className="worm-text">
        {Math.round(percentage)}% of **Billie's** target achieved! That's {current_num_of_books} of {target} books.
      </p>
    </div>
  )

}

export default Milestones
