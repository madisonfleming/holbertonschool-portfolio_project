import { useEffect, useState } from "react";
import { useAuth } from "../../contexts/AuthContext";
import "./child-profiles.css";
import MilestonesChild from "../../components/child-profiles/MilestonesChild";
import MilestonesHistory from "../../components/child-profiles/MilestonesHistory";
import AddReadingSession from "../../components/dashboard/AddReadingSession";
import ChildSelector from "../../components/child-profiles/ChildSelector";
import ExportButton from "../../components/child-profiles/ExportButton";
import { useChild } from "../../contexts/ChildContext";
import { useBooks } from "../../contexts/BooksContext";
import UpdateReadingSessions from "../../components/child-profiles/UpdateReadingSessions";
import book from "../../../public/book.png";

const ChildProfiles = () => {
  const [buttonAddReadingSessionPopup, setButtonAddReadingSessionPopup] =
    useState(false);
  const { selectedChild, childList } = useChild();

  //data for export rewards certificate
  const certificateData = {
    childName: "Billie",
    milestone: "200 Books",
    date: "21.02.26",
  };

  const [selectedBook, setSelectedBook] = useState("");
  const { BooksList } = useBooks();
  const [editingReadingSession, setEditingReadingSession] = useState(null);
  const { readingSessions, updateReadingSessions } = useBooks();
  //const { allReadingSessionPerChild } = useBooks();

  const [buttonUpdateReadingSessionPopup, setButtonUpdateReadingSessionPopup] =
    useState(false);

  return (
    <div>
      <div className="reading-session-container">
        <img
          src={`open-book.png`}
          className="open-book-img"
          onClick={() => setButtonAddReadingSessionPopup(true)}
          type="button"
        />
        <p className="reading-text">Add Reading Session</p>
      </div>
      <h1 className="child-profile-title">Child Profiles</h1>
      <AddReadingSession
        trigger={buttonAddReadingSessionPopup}
        setTrigger={setButtonAddReadingSessionPopup}
        children_RS={childList}
      ></AddReadingSession>
      <div>
        <ChildSelector />
      </div>
      {/* MILESTONES CHILD AND MILESTONS HISTORY */}
      {/* The container is for both cards */}
      <div className="milestones-container">
        <MilestonesChild
          selectedChild={selectedChild}
          certificateData={certificateData}
        />
        <MilestonesHistory selectedChild={selectedChild} />
      </div>
      <div className="reading-activity">
        <div className="reading-activity-h1"> Your Reading Activity </div>
        <div className="book-scroll-container">
          <div className="book-grid">
            {readingSessions.map((session) => (
              <div className="book-item" key={session.id}>
                <img src={session?.img || book} alt={session.title} />
                <p>{session.title}</p>
                {/* update reading session button */}
                <button
                  className="update-reading-sessions-btn"
                  onClick={() => {
                    setEditingReadingSession(session.id);
                    setButtonUpdateReadingSessionPopup(true);
                  }}
                >
                  Edit
                </button>
              </div>
            ))}
          </div>
          {/* if popup is true then render update */}
          {setButtonUpdateReadingSessionPopup && (
            <UpdateReadingSessions
              trigger={buttonUpdateReadingSessionPopup}
              setTrigger={setButtonUpdateReadingSessionPopup}
              updateReadingSessions={updateReadingSessions}
              readingSessions={readingSessions}
              data={editingReadingSession}
            ></UpdateReadingSessions>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChildProfiles;
