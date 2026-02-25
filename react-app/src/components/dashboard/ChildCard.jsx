import "./childCard.css"
import { useState } from 'react';
import { Link } from 'react-router-dom';
import GetWorm from "./GetWorm";

/*We dont need to pass the array of kids just using the props to card receives props and shows them */
const ChildCard = ({ name, avatar, age }) => {
  const [isExpanded, setIsexpanded] = useState(false);

  return (
    <div className="child-card">
      <div onClick={() => setIsexpanded(!isExpanded)} aria-expanded={isExpanded}>
      <img className="avatar" src={avatar} alt="avatar" />
      <div className="text">
        <Link className="child-name" to="/child-profiles">{name}</Link>
        <h2 className="child-age">Age: {age}</h2>
      </div>
      </div>
      <div className={`expanded-content ${isExpanded ? 'open' : ""}`}>
      <GetWorm />
      </div>
      
    </div>
  )
}
export default ChildCard;
