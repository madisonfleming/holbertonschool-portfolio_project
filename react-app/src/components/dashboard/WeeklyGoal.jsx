import "./WeeklyGoal.css";
const WeeklyGoal = ({ theme, target }) => {
  return (
    <div className="weekly-goal-card">
      <div className="main-part">
        <div className="week-banner">
          <span className="week-line">THIS WEEK</span>
        </div>
         <h1 className="main-part-title">It's <em><strong>{theme}</strong></em> Week!</h1>
         <div className="image-wrap">
          <img src={`/themes/${theme}.png`} alt={theme} />
          </div>
         <div className="tagline">Big stories from gentle giants</div>
      </div>

      <div className="text-button">
        <h3>Big stories form gentle giants</h3>
        <h4>
          Read {target} books about <strong>{theme}</strong> this week to earn
          the reward!
        </h4>
        <button className="complete-btn">Complete</button>
      </div>
    </div>
  );
};

export default WeeklyGoal;
