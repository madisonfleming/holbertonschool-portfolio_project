import "./childCard.css"
import { useState } from 'react';
import { Link } from 'react-router-dom';
import GetWorm from "./GetWorm";
import { useChild } from "../../contexts/ChildContext";

// now recieving data from usechild context
const ChildCard = ({ onEdit}) => {
  const [expandedChild, setExpandedChild] = useState(null);
  const { childList } = useChild();

  return (
    <div className="child-container">
      {childList.map((child) => {
    const isOpen = expandedChild === child.id;

    return (
      <div key={child.id}>
      {/* BUTTON FOR TEST UPDATE CHILD */}
      <button onClick={() => onEdit(child)}>Edit</button>
      <div className="child-card" onClick={() => setExpandedChild(isOpen ? null : child.id)} aria-expanded={isOpen}>
              <img src={child.avatar_url} alt={child.name} className="child-avatar" /> 
            <div className="text">
              <Link className="child-name" to="/child-profiles" onClick={(e) => e.stopPropagation()}>{child.name}</Link>
              <div className="child-age">{child.age}</div>
            </div>
      <div className={`expanded-content ${isOpen ? 'open' : ""}`}>
        <GetWorm />
      </div>
      </div>
      </div>
    );
  })}
      </div>
    )
}
export default ChildCard;

{/*<img className="avatar" src={selectedChild.avatar} alt="avatar" />
      <div className="text">
        <Link className="child-name" to="/child-profiles">{selectedChild.name}</Link>
        <h2 className="child-age">Age: {selectedChild.age}</h2>
      </div>
      </div>
      <div className={`expanded-content ${isExpanded ? 'open' : ""}`}>
      <GetWorm />
      </div>
      
    </div>
    </div>
      ) */}


