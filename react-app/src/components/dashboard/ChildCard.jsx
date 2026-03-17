import "./childCard.css";
import { useState } from "react";
import { Link } from "react-router-dom";
import GetWorm from "./GetWorm";
import { useChild } from "../../contexts/ChildContext";

// now recieving data from usechild context
const ChildCard = () => {
  const [expandedChild, setExpandedChild] = useState(null);
  const { childList, selectedChild, setSelectedChild } = useChild();

  return (
    <div className="child-container">
      {childList.map((child) => {
        const isOpen = expandedChild === child.id;

        return (
          <div key={child.id}>
            <div
              className="child-card"
              onClick={() => {
                setExpandedChild(isOpen ? null : child.id);
                setSelectedChild(child);
              }}
              aria-expanded={isOpen}
            >
              <div className="row-layout">
                <img
                  src={child.avatar}
                  alt={child.name}
                  className="child-avatar"
                />
                <div className="text">
                  <Link
                    className="child-name"
                    to="/child-profiles"
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedChild(child);
                    }}
                  >
                    {child.name}
                  </Link>
                  <div className="child-age">Age: {child.age}</div>
                  <p className="info-desc">
                    <strong>Click here </strong>to see the progress!
                  </p>
                </div>
              </div>
              <div className={`expanded-content ${isOpen ? "open" : ""}`}>
                <GetWorm selectedChild={selectedChild} />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
export default ChildCard;

{
  /*<img className="avatar" src={selectedChild.avatar} alt="avatar" />
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
      ) */
}
