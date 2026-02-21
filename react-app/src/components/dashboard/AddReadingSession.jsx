
import './AddReadingSession.css'
import { useState, useEffect } from "react";


const AddReadingSession = (props) => {
  const child_list = props.children_RS || [];
  const books = [
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" },
    { title: "Where the Wild Things Are", img: "/books/wild-things.png" },
    { title: "Matilda", img: "/books/matilda.png" }

  ];

  const [searchTerm, setSearchTerm] = useState("");
  const [selectedBook, setSelectedBook] = useState(null);
  const [date, setDate] = useState("");
  const [selectedChild, setSelectedChild] = useState(null);

  const filteredBooks = books.filter(book =>
    book.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  {/* with this trigger we reset to today date when closing the card */ }
  useEffect(() => {
    if (props.trigger) {
      const today = new Date().toISOString().split("T")[0];
      setDate(today);
    }
  }, [props.trigger]);

  useEffect(() => {
    if (props.trigger) {
      setSelectedBook("");     // reset book
      setSearchTerm("");       // reset search input (si lo usas)
    }
  }, [props.trigger]);


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

        <div className="reading-session-layout">

          {/* --- BOOK SELECTOR --- */}
          <div className="left-section">

            <h4>Search for your book</h4>
            <input
              type="text"
              className="select-field"
              placeholder="Start typing..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            {searchTerm && (
              <div className="dropdown-list">
                {filteredBooks.map((book, index) => (
                  <div
                    key={index}
                    className="dropdown-item"
                    onClick={() => {
                      setSelectedBook(book);
                      setSearchTerm(book.title); // shows the selected book
                    }}
                  >
                    {book.title}
                  </div>
                ))}

                {filteredBooks.length === 0 && (
                  <div className="dropdown-item no-results">No matches found</div>
                )}
              </div>
            )}

            {/* --- DATE SELECTOR --- */}
            <h4>Select a date</h4>
            <input type="date" className="select-field" id="date" value={date} onChange={(e) => setDate(e.target.value)} />
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
          <button className="btn btn-s" onClick={() => props.setTrigger(false)}>Close</button>
          <button className="btn btn-s">Submit Reading Session</button>
        </div>
      </div>
    </div>
  ) : "";
}

export default AddReadingSession