import { useState, useEffect } from "react";
import "./UpdateReadingSession.css"
import { useBooks } from "../../contexts/BooksContext";
import { useChild } from "../../contexts/ChildContext";

const UpdateReadingSessions = ({ trigger, setTrigger, readingSessions, data, updateReadingSessions }) => {
  //data prop for reading session ID
  //add updateReadingSessions as a prop rather than call from context

  //using selectedChild from child context ie using the child in the current state
  const { childList, selectedChild } = useChild();
  //this take the states that receive as a prop (readingSessions) 
  const [sessionId, setSessionId] = useState(readingSessions?.id || "");
  const [date, setDate] = useState(readingSessions?.logged_at || "");
  const [selectedBook, setSelectedBook] = useState(readingSessions?.book_id || "");
  //set image so it loads immediately
  const [image, setImage] = useState(readingSessions?.cover_url || './book.png');
  //have the child pre selected using the selectedChild's child state 
  const [selectedChildId, setSelectedChildId] = useState(selectedChild?.id || "");

  /* SEARCH BOOKS  */
  const { searchBooks } = useBooks();
  const [searchTerm, setSearchTerm] = useState("");
  const [showDropdown, setShowDropdown] = useState(false);
  const [filteredBooks, setFilteredBooks] = useState([]);

  //sync state when reading session changes
  useEffect(() => {
    if (readingSessions) {
      setSessionId(readingSessions.id || "");
      setDate(readingSessions.logged_at || "");
      setSelectedBook(readingSessions.book_id || "");
      setImage(readingSessions.cover_url || "");
      //update when selectedChild changes 
      setSelectedChildId(selectedChild.id || "");
    }
  }, [readingSessions], [selectedChild]);


  const handleUpdateReadingSession = () => {
    const updatedData = {};

    if (date) {
      updatedData.logged_at = date;
    }
    if (selectedBook) {
      //data sent to backend
      //response payload includes external_id so we use external_id here
      updatedData.external_id = selectedBook.external_id;
      updatedData.title = selectedBook.title;
      updatedData.author = selectedBook.author;
      updatedData.cover_url = selectedBook.img;
    }

    console.log("sending update data for test: ", updatedData);
    console.log("session_id holds:", data)
    //readingSessions are stored with session_id in backend so we need session_id here
    updateReadingSessions(data, updatedData);

    //print the state of reading sessions
    console.log("readingSessions holds:", readingSessions);
    setTrigger(false); // close popup
  };

  const handleCloseResetData = () => {
    setSessionId("");
    setDate("");
    setSelectedBook("");
    setTrigger(false); // close popup
  }
  if (!readingSessions) return null


  return trigger ? (
    <div className="popup-overlay">
      <div className="UpdateReadingSessions">
        {/* Close btn */}
        <button
          className="btn-close"
          onClick={handleCloseResetData}
        >✕
        </button>
        {/* update reading sessions */}
        <h1 className="tittle-popup-card">Update Reading Session</h1>
        <div className="reading-session-layout">
          {/* --- BOOK SELECTOR --- */}
          <div className="left-section">
            {/* --- USER BUTTONS --- */}
            <p className="subtittle-popup-card">Bookworm</p>
            <div className="readers-row">
              {/* recieving the current selectedChildId from the state so pre selected child, and allowing change */}
              {childList.map((child) => (
                <div
                  key={child.id}
                  className={`child-wrapper ${selectedChildId === child.id ? "selected" : ""}`}
                  onClick={() => setSelectedChildId(child.id)}
                >
                  <button className="child-btn">
                    <img src={child.avatar} className="child-avatar-img-rs" />
                  </button>

                  <div className="child-name-inside-card">{child.name}</div>
                </div>
              ))}
            </div>
            <div className="divider"></div>
            {/* --- SEARCH FOR BOOK AND DATE --- */}
            <p className="subtittle-popup-card">Search Book & Date</p>
            <input
              type="text"
              className="select-field"
              placeholder="Search for your book..."
              value={searchTerm}
              onChange={async (e) => {
                setSearchTerm(e.target.value);
                {
                  /* update what the user writes */
                }
                setShowDropdown(true);
                {
                  /* if user deletes the text doest call the be so empty [] */
                }
                if (e.target.value.trim() === "" || e.target.value.length < 2) {
                  setFilteredBooks([]);
                  return;
                }
                {
                  /* here we call the BE -> e.target.value= cat to is search?q=cat, then saved the results so filteredBooks can have books  */
                }
                const results = await searchBooks(e.target.value);
                setFilteredBooks(results);
              }}
            />
            {showDropdown && searchTerm && (
              <div className="dropdown-list">
                {filteredBooks.map((book) => (
                  <div
                    className="dropdown-item"
                    onClick={() => {
                      setSelectedBook(book);
                      setSearchTerm(book.title); // shows the selected book on search..
                      //set image so its stays in the state
                      setImage(book.img)
                      setShowDropdown(false); //disappear the drop down
                    }}
                  >
                    {book.title}
                  </div>
                ))}

                {filteredBooks.length === 0 && (
                  <div className="dropdown-item no-results">
                    No matches found
                  </div>
                )}
              </div>
            )}

            {/* --- DATE SELECTOR --- */}
            <input
              type="date"
              className="select-field"
              id="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
          </div>
          {/*For the img  */}
          <div className="right-section">
            <p className="subtittle-popup-card">Selected Book</p>
            <div className={`book-empty ${selectedBook ? "hidden" : ""}`}>
              <div className="book-empty-text">No book selected yet</div>
              <div className="book-empty-sub">
                Search on the left to find your book
              </div>
            </div>
            <div className={`book-selected ${selectedBook ? "visible" : ""}`}>
              {selectedBook && (
                <img
                  src={selectedBook.img}
                  alt={selectedBook.title}
                  className="book-preview-img"
                />
              )}
            </div>
          </div>
        </div>

        <div className="button-section">
          <button className="btn-submit" onClick={handleUpdateReadingSession}>Update Reading Session</button>
        </div>
      </div>
    </div>
  ) : (
    ""
  );
};
export default UpdateReadingSessions;
