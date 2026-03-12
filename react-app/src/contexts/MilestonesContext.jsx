//this file create e global context and every component can have access using useMilstones the hook
import React, { useState, useEffect, useContext } from "react";
import { useAuth } from "./AuthContext";
import { useChild } from "./ChildContext";
//create a new context object with defalt value null
const MilestonesContext = React.createContext()

//a hook
export function useMilestones() {
    return useContext(MilestonesContext);
}

export function MilestonesProvider({ children }) {
  //need it to access to child.id
 // const { childList } = useChild();
  const { currentUser } = useAuth();
    
  //ENDPOINT TO post once the complete books weekly challenge is clicked
  async function completeWeeklyMilestone(child_id, weeklyMilestoneData) {
    console.log("Payload sent to BE for test completeWeeklyMilestones", weeklyMilestoneData);

    if (!currentUser) return;

    const token = await currentUser.getIdToken();
    const response = await fetch(`http://127.0.0.1:8000/api/children/${child_id}/milestones`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`, 
      },
      body: JSON.stringify(weeklyMilestoneData),
    });
    if (!response.ok) {
      console.error("Error posting the complete weekly milestone");
      return;
    }
    const newCompleteWeeklyMilestone = await response.json();
    console.log("Answer from BE of posting complete weekly rewards:", newCompleteWeeklyMilestone);
  }

  //ENPOINT TO Get ALL milestones attached to a child to get one http://127.0.0.1:8000/api/children/${child_id}/milestones?limit=1
  async function allMilestonesPerChild(child_id) {
   
    if (!currentUser) return;

    const token = await currentUser.getIdToken();
    const response = await fetch(`http://127.0.0.1:8000/api/children/${child_id}/milestones`, 
      {
        headers:
          {
            Authorization: `Bearer ${token}`,
          },
      });
      if (!response.ok) {
      console.error("Error getting all milestones");
      return;
      }
      const milestonesDataChild = await response.json();
      console.log("Answer from BE of all the milestone data from child", milestonesDataChild);
      
    return milestonesDataChild;
  }


    return (
        
        <MilestonesContext.Provider 
        value={{ completeWeeklyMilestone, allMilestonesPerChild}}>
          {children}
        </MilestonesContext.Provider>
    )

}
