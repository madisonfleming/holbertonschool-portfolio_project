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
          date_of_birth={child.date_of_birth}
        />
      ))}
    </div>
  );
};
export default ChildList;
