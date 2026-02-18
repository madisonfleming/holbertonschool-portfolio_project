import "./childCard.css"
import { Link } from 'react-router-dom';
import GetWorm from "./GetWorm";

/*We dont need to pass the array of kids just using the props to card receives props and shows them */
const ChildCard = ({ name, age, avatar, lastReadBook }) => {

  return (
    <div className="child-card">
      <img className="avatar" src={avatar} alt="avatar" />
      <div className="text">
        <Link className="child-name" to="/child-profiles">{name}</Link>
        <h2 className="child-age">Age: {age}</h2>
        <p className="last-read-book">Last Read Book: {lastReadBook}</p>
      </div>
      <div className="worm">
      <GetWorm />
      </div>
    </div>
  )
}
export default ChildCard;
