
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


