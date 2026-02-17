import "./childCard.css"
import ChildCard from "./ChildCard";

const ChildList = ({ child_list }) => {

  return (
    <div className="child-list-container">
      {child_list.map((child) => (
        <ChildCard
          key={child.id}
          name={child.name}
          age={child.age}
          avatar={child.avatar}
          lastReadBook={child.lastReadBook}
        />
      ))}
    </div>
  );
};
export default ChildList;