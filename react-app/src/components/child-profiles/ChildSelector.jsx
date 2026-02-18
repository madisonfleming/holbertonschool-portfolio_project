import { useState } from 'react';

const ChildSelector = ({ children_RS, selectedChildId, setSelectedChildId }) => {
    const child_list = children_RS || [];
    /* using selectedChildId so that parent child-profile get selected id */

    return (
        <div>
          <div className="child-selector">
            <select className="child-dropdown"
            value={selectedChildId || ""}
            onChange={(e) => setSelectedChildId(Number(e.target.value))} >
                {/*<option value="" disabled>Wormies</option>*/}
          {child_list.map((child) => (
            <option
              key={child.id}
              value={child.id}
              className={`child-btn ${selectedChildId === child.id ? "active" : ""}`}
              onClick={() => setSelectedChildId(child.id)}
            >
              {child.name}
            </option>
          ))}
        </select>
        </div>
        </div>
    )
}
export default ChildSelector

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
