import "./AddReadingSession.css";
import { useState, useEffect } from "react";

const AddReadingSession = (props) => {
  const child_list = props.children_RS || [];
  const books = [
    {
      title: "The Very Hungry Caterpillar",
      img: "public/books/caterpillar.png",
    },
    { title: "Where the Wild Things Are", img: "/books/wild-things.png" },
    { title: "Matilda", img: "/books/matilda.png" },
  ];

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
      setSelectedBook(""); // reset book
      setSearchTerm(""); // reset search input (si lo usas)
    }
  }, [props.trigger]);

  return props.trigger ? (
    <div className="popup-overlay">
      <div className="AddReadingSessionCard">
        <h1>Log a reading session</h1>

        <div className="reading-session-layout">
          {/* --- BOOK SELECTOR --- */}
          <div className="left-section">
            {/* --- USER BUTTONS --- */}
            <h4>BOOKWORM</h4>
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

            {/* --- SEARCH FOR BOOK --- */}
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
            {selectedBook && (
              <img
                src={selectedBook.img}
                alt={selectedBook.title}
                className="book-preview-img"
              />
            )}
          </div>
        </div>
        {props.children}
        <div className="button-section">
          <button className="btn btn-s" onClick={() => props.setTrigger(false)}>
            Close
          </button>
          <button className="btn btn-s">Submit Reading Session</button>
        </div>
      </div>
    </div>
  ) : (
    ""
  );
};

export default AddReadingSession;
