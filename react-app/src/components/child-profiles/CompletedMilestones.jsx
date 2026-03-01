

const CompletedMilestones = ({ completedMilestones }) => {
    const milestones = completedMilestones || [];



    return (
        <div className="milestone-list">
              {milestones.map((milestone) => (
                <div key={milestone.id}>
                    <img className="star" src={"/mini_star.svg"}></img>
                  {milestone.name}
                </div>
              ))}
            </div>
    )
}
export default CompletedMilestones;
