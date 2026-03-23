import "./ChildCardSettings.css"
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useChild } from "../../contexts/ChildContext";
import UpdateChild from "../../components/dashboard/UpdateChild";
import { useAuth } from "../../contexts/AuthContext";

// now recieving data from usechild context
const ChildCard = () => {
  const { childList, updateChild } = useChild();
  const [buttonUpdateChildPopup, setButtonUpdateChildPopup] = useState(false);
  const [editingChild, setEditingChild] = useState(null);

  const { selectedChild } = useChild();
  const { currentUser } = useAuth();

  return (
    <div>
      {childList.map((child) => {
        return (
          <div key={child.id}>
            <div className="child-card-settings">
              <img src={child.avatar} alt={child.name} className="child-avatar-settings" />
              <div className="child-info">
                <Link className="child-name-settings" to="/child-profiles" onClick={(e) => e.stopPropagation()}>{child.name}</Link>
                <div className="child-age-settings">{child.age} years</div>
              </div>
              {/* updateChild buttom for testing */}
              <button className="btn-update-settings"
                onClick={() => {
                  setEditingChild(child);
                  setButtonUpdateChildPopup(true);
                }}
              >Update
              </button>
              {/* Invite User button ONLY VISIBLE FOR PRIMARY USER NOT POSSIBLE W STANDARD USER */}
              {currentUser.uid === "CVelQleFzqXvvuLQGllEnP4FnhD2" && (
                <button className="btn-update-settings">Invite</button>
              )}

            </div>
          </div>
        );
      })}
      {/* Im saying if popup is true then render update */}
      {setButtonUpdateChildPopup && (
        <UpdateChild
          trigger={buttonUpdateChildPopup}
          setTrigger={setButtonUpdateChildPopup}
          updateChild={updateChild}
          child={editingChild}
        ></UpdateChild>
      )}
    </div>
  )
}
export default ChildCard;



