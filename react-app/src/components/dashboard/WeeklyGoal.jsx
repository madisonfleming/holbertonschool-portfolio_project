import "./WeeklyGoal.css";
import { useState, useEffect } from "react";

const WeeklyGoal = ({ theme, target }) => {

  /* In order to mark many books we need an array */
  const [selectedBooks, setSelectedBooks] = useState(Array(target).fill(false));
  /*to populate the books */
  const goalBooks = [];
  let cont = 0;
  while (cont < target) {
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

  /*To detect that all of them are checked on an arrow function books is each value true or false, if all are true return true  */
  const allCompleted = selectedBooks.every(books => books === true);

  /* handle reset each time we export reward */
  const handleResetData = () => {
    setSelectedBooks(Array(target).fill(false));
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
          <button 
            className={`btn-reward ${allCompleted ? "active" : "disabled"}`}
            disabled={!allCompleted}
            onClick={handleResetData}
            >
            {allCompleted ? "Claim Reward! Click to export" : "Complete all books to unlock reward"}

          </button>

      </div>

    </div>
  );
};

export default WeeklyGoal;
