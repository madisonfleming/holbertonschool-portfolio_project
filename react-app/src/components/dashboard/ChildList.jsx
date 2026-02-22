import "./childCard.css";
import ChildCard from "./ChildCard";

const ChildList = ({ child_list }) => {
  return (
    <div className="child-list-container">
      {child_list.map((child) => (
        <ChildCard
          key={child.id}
          name={child.name}
          avatar={child.avatar}
          age={child.age}
        />
      ))}
    </div>
  );
};
export default ChildList;
