
import './AddReadingSession.css'
import { useState } from "react";


const AddReadingSession = (props) => {
  const child_list = props.children_RS || [];
  const books = [
    "The Very Hungry Caterpillar",
    "Where the Wild Things Are",
    "Goodnight Moon",
    "The Gruffalo",
    "Green Eggs and Ham",
    "The Cat in the Hat",
    "Corduroy",
    "Brown Bear, Brown Bear, What Do You See?",
    "The Snowy Day",
    "Matilda"
  ];

  const [selectedBook, setSelectedBook] = useState("");
  const [date, setDate] = useState("");
  const [selectedChild, setSelectedChild] = useState(null);




  return (props.trigger) ? (
    <div className="popup-overlay">
      <div className="AddReadingSessionCard">
        <h1>Log a reading session</h1>
        {/* --- USER BUTTONS --- */}
        <h2>Bookworm:</h2>
        <div className="child-buttons">
          {child_list.map((child) => (
            <button
              key={child.id}
              className={`child-btn ${selectedChild === child.id ? "active" : ""}`}
              onClick={() => setSelectedChild(child.id)}
            >
              {child.name}
            </button>
          ))}
        </div>

        {/* --- BOOK SELECTOR --- */}
        <h4>Search for your book</h4>
        <select className="select-field" value={selectedBook} onChange={(e) => setSelectedBook(e.target.value)}>
          <option value="">Search...</option>
          {books.map((title, index) => (<option key={index} value={title}>{title}</option>
          ))}
        </select>
        <h4>Select a date</h4>
        <input type="date" className="select-field" id="date" value={date} onChange={(e) => setDate(e.target.value)} />
        {props.children}
        <div className="button-section">
          <button className="btn btn-s" onClick={() => props.setTrigger(false)}>Close</button>
          <button className="btn btn-s">Submit Reading Session</button>
        </div>
      </div>
    </div>
  ) : "";
}

export default AddReadingSession