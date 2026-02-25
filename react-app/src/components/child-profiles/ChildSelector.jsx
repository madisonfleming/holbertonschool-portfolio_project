import { useState, useRef, useEffect } from 'react';
import './ChildSelector.css'
import { useChild } from '../../contexts/ChildContext';

const ChildSelector = () => {
//    const child_list = children_RS || [];
    const { childList, selectedChild, setSelectedChild } = useChild();
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef(null);

    //main selection function
    const handleSelect = (selectedChild) => {
//      console.log("clicked child", selectedChild)
      setSelectedChild(selectedChild);
      console.log("selectedchild holds:", selectedChild)
      setIsOpen(false);
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
          {selectedChild ? selectedChild.name : "Wormies"}
          <img src="/arrow.svg" alt="arrow" className="arrow"></img>
        </div>
        {isOpen && (
          <div className="dropdown-list">
            {childList.map((child) => (
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
