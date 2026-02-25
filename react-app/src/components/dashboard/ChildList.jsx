import "./childCard.css"
import ChildCard from "./ChildCard";

const ChildList = ( props ) => {
//fix passing { props } from childrenData in parent file to child_list. if no child render empty
  const child_list = props.childrenData || [];

  return (
    <div>
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
