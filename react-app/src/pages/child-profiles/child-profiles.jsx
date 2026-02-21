import { useEffect, useState } from "react";
import { useAuth } from '../../contexts/AuthContext'
import "./child-profiles.css";
import Milestones from '../../components/dashboard/Milestones';
import AddReadingSession from "../../components/dashboard/AddReadingSession";
import ChildSelector from "../../components/child-profiles/ChildSelector";


const ChildProfiles = () => {
    const [buttonAddReadingSessionPopup, setButtonAddReadingSessionPopup] = useState(false);
    const current_num_of_books = 100;   
    const target = 1000;
    const children = [
    { id: 1, name: 'Billie', age: 3, avatar: "/star.svg", lastReadBook: "My Little Pony" },
    { id: 2, name: 'Hannah', age: 3, avatar: "/star.svg", lastReadBook: "My Little Bookworm" },
    { id: 4, name: 'Gia', age: 3, avatar: "/star.svg", lastReadBook: "My Little Kitten" },
  ];

  const books = [
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" },
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" },
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" },
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" },
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" },
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" },
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" },
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" },
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" },
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" },
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" },
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" },
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" },
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" },
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" },
    { title: "The Very Hungry Caterpillar", img: "public/books/caterpillar.png" }
  ];

  const [selectedBook, setSelectedBook] = useState("");
  return (
    <div>
      <div className="reading-session-container">
        <img src={`open-book.png`} className="open-book-img" onClick={() => setButtonAddReadingSessionPopup(true)} type="button" />
        <p className="reading-text">Add Reading Session</p>
      </div>
      <h1 className="child-profile-title">Child Profiles</h1>
      <AddReadingSession trigger={buttonAddReadingSessionPopup} setTrigger={setButtonAddReadingSessionPopup} children_RS={children}>
      </AddReadingSession>
      <div className="child-profiles-grid">
        <div className="children-container">
          <ChildSelector children_RS={children} />
                          {/* for letting the parent hold the child id
                          selectedChildId={selectedChildId} 
                            setSelectedChildId={setSelectedChildId} */} 
        </div>
        <div className="weekly-container">
        </div>
        <div className="milestones-container">
          <Milestones current_num_of_books={current_num_of_books} target={target} />
        </div>
      </div>
      <div className="reading-activity">
        <div className="reading-activity-h1"> Your Reading Activity </div>
       <div className="book-scroll-container">
        <div className="book-grid">
          {books.map((book, index) => (
          <div className="book-item" key={index}>
            <img src={book.img} alt={book.title} />
          <p>{book.title}</p>
        </div>
        ))}
        </div>
      </div>
      </div>
    </div>
  )
}

export default ChildProfiles

