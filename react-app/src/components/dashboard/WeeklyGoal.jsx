import "./WeeklyGoal.css";
const WeeklyGoal = ({ theme, current_num_of_books, target }) => {
  return (
    <div className="weekly-goal-card">
      <h2>It's {theme} Week!</h2>
      <img src={`/themes/${theme}.png`} alt={theme} className="theme-img" />
      <h3>Target: </h3>
      <h3>
        Read {target} books about <strong>{theme}</strong> this week to earn the
        reward!
      </h3>
      <h3> Finished? Click in complete </h3>
      <button>Complete</button>
    </div>
  );
};

export default WeeklyGoal;
