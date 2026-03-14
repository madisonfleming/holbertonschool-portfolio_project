import "./WeeklyGoal.css";
import { useChild } from "../../contexts/ChildContext";
import { useMilestones } from "../../contexts/MilestonesContext";
import { useState, useEffect } from "react";

const WeeklyGoal = ({ theme, target }) => {

  const { completeWeeklyMilestone } = useMilestones();

  const { childList } = useChild();
  //selected child for weekly reward
  const [selectedChild, setSelectedChild] = useState(null);
  /* In order to mark many books we need an array */
  const [selectedBooks, setSelectedBooks] = useState(Array(target).fill(false));
  /*To detect that all of them are checked on an arrow function books is each value true or false, if all are true return true  */
  let allCompleted = selectedBooks.every(books => books === true);
  //transform from True to the required string to the BE
  if (allCompleted){
    allCompleted = "elephants";
  }

  /*to populate the books */
  const goalBooks = [];

  let cont = 1;
  while (cont <= target) {
    goalBooks.push(
      <img 
        key={cont}
        src="open-book.png"
        className="book-circle-img"
      />
    );
    cont++;
  }

  /* we need to keep handle every select one and saved */
  const handleSelectBook = (index) => {
    setSelectedBooks(prev => {
      const updated = [...prev];
      updated[index] = true; //its true so is clicked
      return updated;
    });
  };
  /* handle reset each time we export reward, we need two arguments child_id and the {} as weeklyMilestonsData*/
  const handleCompleteWeeklyMilestone = () => {
     completeWeeklyMilestone(
      selectedChild, 
      {
      child_id: selectedChild,
      subject: allCompleted,
    });
   
    setSelectedBooks(Array(target).fill(false));
    setSelectedChild(null);
  };


  return (
    <div className="weekly-goal-card">
      <div className="main-part">
        <div className="week-banner">
          <span className="week-line">THIS WEEK</span>
        </div>
         <h1 className="main-part-title">It's 
          <em><strong> {theme}</strong></em><br />
           Week!
            </h1>
         <div className="image-wrap">
          <img src={`/themes/${theme}.png`} alt={theme} />
          </div>
         <div className="tagline">Keep reading, keep growing!</div>
      </div>

      <div className="info">
        <p className="info-desc">
          Read <strong>{target} books</strong> about <strong>{theme}</strong> this week to earn
          the reward!
        </p>
        {/* BOKKS PART */}
        <div className="tracker-label">Bookworm</div>
        <div className="books-row">
          {childList.map((child) => (
                <div
                  key={child.id}
                  className={`child-wrapper ${selectedChild === child.id ? "selected" : ""}`}
                  onClick={() => setSelectedChild(child.id)}
                >
                  <button className="child-btn">
                    <img src={child.avatar} className="child-avatar-img-rs" />
                  </button>
                  <div className="child-name-inside-card">{child.name}</div>
                </div>
              ))}
        </div>
        {/* BOKKS PART */}
        <div className="tracker-label">Books completed</div>
        <div className="books-row">
          {goalBooks.map((book, index) => (
            <div 
              className={`book-circle ${selectedBooks[index] ? "selected" : ""}`}
              key={index}
              onClick={() => handleSelectBook(index)}
              >
              {book} {/*this is the call to our img in push, render the img here */}
            </div>
          ))}
        </div>
        {/* SUBMIT BUTTON */}
          <button 
            className={`btn-reward ${allCompleted ? "active" : "disabled"}`}
            disabled={!allCompleted}
            onClick={handleCompleteWeeklyMilestone}
            >
            {allCompleted ? "Claim Reward! Click to export" : "Complete all books to unlock reward"}

          </button>

      </div>

    </div>
  );
};

export default WeeklyGoal;
