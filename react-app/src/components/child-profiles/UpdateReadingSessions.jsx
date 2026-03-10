import { useState, useEffect } from "react";
import "./UpdateReadingSession.css"
import { useBooks } from "../../contexts/BooksContext";
import { useChild } from "../../contexts/ChildContext";

const UpdateReadingSessions = ({ readingSessions, trigger, setTrigger }) => {

    //this take the states that receive as a prop (child) so when the pop up opne it fills with child info
    const [childName, setChildName] = useState(readingSessions?.child_id || "");
    const [date, setDate] = useState(readingSessions?.logged_at || "");
    const [selectedBook, setSelectedBook] = useState(readingSessions?.book_title || "");

      /* SEARCH BOOKS  */
      const { searchBooks, updateReadingSessions } = useBooks();
      const { childList } = useChild();
      const [searchTerm, setSearchTerm] = useState("");
      const [showDropdown, setShowDropdown] = useState(false);
      const [selectedChild, setSelectedChild] = useState(null);
      const [filteredBooks, setFilteredBooks] = useState([]);

      if (!readingSessions) return null;

    useEffect(() => {
        if (readingSessions) {
            setChildName(readingSessions.child_id || "");
            setDate(readingSessions.logged_at || "");
            setSelectedBook(readingSessions.book_title || "");
        }
    }, [readingSessions]);

    /*
    useEffect(() => {
      if (props.trigger) {
        setSelectedBook(null);
        setSearchTerm("");
    }
  }, [props.trigger]);
*/

    const handleUpdateReadingSession = () => {
        const updatedData = {};

        if (childName && childName !== readingSessions.child_id) {
            updatedData.name = childName;
        }
        if (date && date !== readingSessions.logged_at) {
            updatedData.logged_at = date;
        }
        if (selectedBook && selectedBook !== readingSessions.book_title) {
            updatedData.book_title = selectedBook
        }
        console.log("sending update data for test: ", updatedData);
        updateReadingSessions(readingSessions.session_id, updatedData);

        setTrigger(false); // close popup
    };

    const handleCloseResetData = () => {
    setChildName("");
    setDate("");
    setSelectedBook("");
    setTrigger(false); // close popup
  }

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
        <h1 className="tittle-popup-card">Update Reading Sessions</h1>
         <div className="reading-session-layout">
            {/* --- BOOK SELECTOR --- */}
           <div className="left-section">
            {/* --- USER BUTTONS --- */}
           <p className="subtittle-popup-card">Bookworm</p>
            <div className="readers-row">
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
