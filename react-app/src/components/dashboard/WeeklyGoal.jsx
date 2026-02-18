import "./WeeklyGoal.css"
const WeeklyGoal = ({ theme, current_num_of_books, target }) => {
  return (
    <div className="weekly-goal-card" >
      <h2>It's {theme} Week!</h2>
      <img src={`/themes/${theme}.png`} alt={theme} className="theme-img" />
      <h3>Read {target} books about <strong>{theme}</strong> to earn the reward!</h3>
      <h3> Progress: {current_num_of_books} / {target} </h3>
    </div>

  )
}

export default WeeklyGoal