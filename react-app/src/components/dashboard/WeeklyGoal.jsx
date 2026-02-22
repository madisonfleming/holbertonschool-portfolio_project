import "./WeeklyGoal.css";
const WeeklyGoal = ({ theme, target }) => {
  return (
    <div className="weekly-goal-card">
      <div className="text-section">
        <h2>It's</h2>
        <h2>{theme}</h2>
        <h2>Week!</h2>
      </div>
      <div className="text-button">
        <h3>Big stories form gentle giants</h3>
        <h4>
          Read {target} books about <strong>{theme}</strong> this week to earn
          the reward!
        </h4>
        <button className="complete-btn">Complete</button>
      </div>
      <img src={`/themes/${theme}.png`} alt={theme} className="theme-img" />
    </div>
  );
};

export default WeeklyGoal;
