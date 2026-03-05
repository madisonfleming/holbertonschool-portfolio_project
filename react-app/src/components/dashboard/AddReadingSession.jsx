import "./AddReadingSession.css";
import { useChild } from "../../contexts/ChildContext"
import { useState, useEffect } from "react";

const AddReadingSession = (props) => {

  const { childList } = useChild();
  const books = [
    {
      title: "The Very Hungry Caterpillar",
      img: "public/books/caterpillar.png",
    },
    { title: "Where the Wild Things Are", img: "/books/wild-things.png" },
    { title: "Matilda", img: "/books/matilda.png" },
  ];

  /*searchTerm for the text the user writes and setSearchTerm to update it  */
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedBook, setSelectedBook] = useState(null);
  const [showDropdown, setShowDropdown] = useState(false);
  const [date, setDate] = useState("");
  const [selectedChild, setSelectedChild] = useState(null);

  const filteredBooks = books.filter((book) =>
    book.title.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  {
    /* with this trigger we reset to today date when closing the card */
  }
  useEffect(() => {
    if (props.trigger) {
      const today = new Date().toISOString().split("T")[0];
      setDate(today);
    }
  }, [props.trigger]);

  useEffect(() => {
    if (props.trigger) {
      setSelectedBook(null); 
      setSearchTerm(""); 
    }
  }, [props.trigger]);

  return props.trigger ? (
    <div className="popup-overlay">
      <div className="AddReadingSessionCard">
        {/*Close btn */}
        <button className="btn-close" onClick={() => props.setTrigger(false)}>
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
                    <img
                      src={child.avatar_url}
                      className="child-avatar-img-rs"
                    />
                  </button>
                   {console.log('avatar test andrea:', child.avatar_url)}
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
              onChange={(e) => {
                setSearchTerm(e.target.value);
                setShowDropdown(true);
              }}
            />
            {showDropdown && searchTerm && (
              <div className="dropdown-list">
                {filteredBooks.map((book, index) => (
                  <div
                    key={index}
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
              <div className="book-empty-sub">Search on the left to find your book</div>
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
        {props.children}
        <div className="button-section">
          <button className="btn-submit">Submit Reading Session</button>
        </div>
      </div>
    </div>
  ) : (
    ""
  );
};

export default AddReadingSession;
