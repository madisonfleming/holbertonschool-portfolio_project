import "./childCard.css";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import GetWorm from "./GetWorm";
import { useChild } from "../../contexts/ChildContext";
import { useBooks } from "../../contexts/BooksContext";

const ChildCard = () => {
  const { childList, setSelectedChild } = useChild();
  const { getReadingSessionsCount } = useBooks();

  const [expandedChild, setExpandedChild] = useState(null);
  const [counts, setCounts] = useState({});

  //Load ALL counts once when childList is available
  useEffect(() => {
    async function loadAllCounts() {
      const newCounts = {};

      for (const child of childList) {
        const count = await getReadingSessionsCount(child.id);
        newCounts[child.id] = count;
      }

      setCounts(newCounts);
    }

    if (childList.length > 0) {
      loadAllCounts();
    }
  }, [childList]);

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

              {isOpen && (
                <div className="expanded-content open">
                  <GetWorm count={counts[child.id] || 0} />
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ChildCard;
