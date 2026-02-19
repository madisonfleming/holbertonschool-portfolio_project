import { useState, useRef, useEffect } from 'react';
import './ChildSelector.css'

const ChildSelector = ({ children_RS, onSelect }) => {
    const child_list = children_RS || [];
    const [isOpen, setIsOpen] = useState(false);
    const [selectedChildId, setSelectedChildId] = useState(null);
    const dropdownRef = useRef(null);

    const handleSelect = (child) => {
      setSelectedChildId(child);
      setIsOpen(false);
//send child id to parent
      if (onSelect) {
        onSelect(child.id);
      }
    };
//if user clicks outside, dropdown closes
    useEffect(() => {
      const handleClickOutside = (event) => {
        if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
          setIsOpen(false);
        }
      };
      document.addEventListener("mousedown", handleClickOutside);
      return () => document.removeEventListener("mousedown", handleClickOutside)
    }, []);

    return (
      <div className="select-container" ref={dropdownRef}>
        <div className="dropdown-header"
        onClick={() => setIsOpen(!isOpen)}>
          {selectedChildId ? selectedChildId.name : "Wormies"}
          <img src="/arrow.svg" alt="arrow" className="arrow"></img>
        </div>
        {isOpen && (
          <div className="dropdown-list">
            {child_list.map((child) => (
              <div key={child.id}
              className="dropdown-item"
              onClick={() => handleSelect(child)}>
                {child.name}
                </div>
            ))}
          </div>
          
        )}

        </div>
    );
  }
  export default ChildSelector;




    /* Child selector half working as select dropdown. styling was impossible
  
    return (
        <div>
          <div className="select-container"> {/* select-container */
            /*<select 
            id="select"
            className="child-dropdown"
            value={selectedChildId || ""}
            onChange={(e) => setSelectedChildId(Number(e.target.value))} >
                <option value="" disabled>Wormies</option>
          {child_list.map((child) => (
            <option
              key={child.id}
              value={child.id}
            >
              {child.name}
            </option>
          ))}
        </select>
        </div>
        </div>
    )
}
*/
/* child selector working as buttons
return (
        <div>
          <div className="child-selector">
          {child_list.map((child) => (
            <button
              key={child.id}
              className={`child-btn ${selectedChildId === child.id ? "active" : ""}`}
              onClick={() => setSelectedChildId(child.id)}
            >
              {child.name}
            </button>
          ))}
        </select>
        </div>
        </div>
    )
}
export default ChildSelector */
