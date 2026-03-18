import "./AddReadingSession.css";
import { useChild } from "../../contexts/ChildContext";
import { useBooks } from "../../contexts/BooksContext";
import { useState, useEffect } from "react";
import { useAuth } from "../../contexts/AuthContext";
import book_img from "../../../public/mlb-book_cover.png";

const AddReadingSession = (props) => {
  const { childList } = useChild();
  const { searchBooks, createReadingSession } = useBooks();

  /*
  const books = [
    {
      title: "The Very Hungry Caterpillar",
      img: "public/books/test.png",
    },
    { title: "Where the Wild Things Are", img: "/books/wild-things.png" },
    { title: "Matilda", img: "/books/matilda.png" },
  ];*/

  /*searchTerm for the text the user writes and setSearchTerm to update it  */
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedBook, setSelectedBook] = useState(null);
  const [showDropdown, setShowDropdown] = useState(false);
  const [date, setDate] = useState("");
  const [selectedChild, setSelectedChild] = useState(null);
  const [filteredBooks, setFilteredBooks] = useState([]);
  const { currentUser } = useAuth();
  // set the image in the state so it loads automatically
  const [image, setImage] = useState("");

  //we need a handle in order to create the obj with the states
  // we need to POST in order to the BE to received name, date_of_birth, avatar_url
  const handleCreateReadingSession = () => {
    createReadingSession({
      child_id: selectedChild,
      external_id: selectedBook.external_id,
      source: selectedBook.source,
      title: selectedBook.title,
      author: selectedBook.author,
      cover_url: selectedBook.img,
      logged_at: date,
    });
    setSearchTerm("");
    setSelectedBook(null);
    setShowDropdown(false);
    //* with this trigger we reset to today date when closing the card */
    const today = new Date().toISOString().split("T")[0];
    setDate(today);
    setSelectedChild(null);
    props.setTrigger(false); // close popup
  };

  //handle to reset the data once we close the card
  const handleCloseResetData = () => {
    setSearchTerm("");
    setSelectedBook(null);
    setShowDropdown(false);
    //* with this trigger we reset to today date when closing the card */
    const today = new Date().toISOString().split("T")[0];
    setDate(today);
    setSelectedChild(null);
    props.setTrigger(false); // close popup
  };

  return props.trigger ? (
    <div className="popup-overlay">
      <div className="AddReadingSessionCard">
        {/*Close btn */}
        <button className="btn-close" onClick={handleCloseResetData}>
          ✕
        </button>
        <h1 className="tittle-popup-card">Log a reading session</h1>

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
                  {console.log("avatar test andrea:", child.avatar)}
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
                      setImage(book.img); //save the image in state
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
                  src={selectedBook.img || book_img}
                  alt={selectedBook.title}
                  className="book-preview-img"
                />
              )}
            </div>
          </div>
        </div>
        {props.children}
        <div className="button-section">
          <button className="btn-submit" onClick={handleCreateReadingSession}>
            Submit Reading Session
          </button>
        </div>
      </div>
    </div>
  ) : (
    ""
  );
};

export default AddReadingSession;
