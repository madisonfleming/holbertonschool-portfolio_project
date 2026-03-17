//this file create e global context and every component can have access using useMilstones the hook
import React, { useState, useEffect, useContext } from "react";
import { useAuth } from "./AuthContext";
import { useChild } from "./ChildContext";
//create a new context object with defalt value null
const MilestonesContext = React.createContext();

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
    console.log(
      "Payload sent to BE for test completeWeeklyMilestones",
      weeklyMilestoneData,
    );

    if (!currentUser) return;

    const token = await currentUser.getIdToken();
    const response = await fetch(
      `http://127.0.0.1:8000/api/children/${child_id}/milestones`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(weeklyMilestoneData),
      },
    );
    if (!response.ok) {
      console.error("Error posting the complete weekly milestone");
      return;
    }
    const newCompleteWeeklyMilestone = await response.json();
    console.log(
      "Answer from BE of posting complete weekly rewards:",
      newCompleteWeeklyMilestone,
    );
  }

  //ENPOINT TO Get ALL milestones attached to a child to get one http://127.0.0.1:8000/api/children/${child_id}/milestones?limit=1
  async function allMilestonesPerChild(child_id) {
    if (!currentUser) return;

    const token = await currentUser.getIdToken();
    const response = await fetch(
      `http://127.0.0.1:8000/api/children/${child_id}/milestones`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );
    if (!response.ok) {
      console.error("Error getting all milestones");
      return;
    }
    const milestonesDataChild = await response.json();
    console.log(
      "Answer from BE of all the milestone data from child",
      milestonesDataChild,
    );

    return milestonesDataChild;
  }

  //ENPOINT TO Get ONLY WEEKLY GOAL http://127.0.0.1:8000/api/children/${child_id}/milestones?limit=1
  async function weeklyGoalMilestonesPerChild(child_id) {
    if (!currentUser) return;

    const token = await currentUser.getIdToken();
    const response = await fetch(
      `http://127.0.0.1:8000/api/children/${child_id}/milestones?type=weekly_goal`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );
    if (!response.ok) {
      console.error("Error getting weekly goal milestones");
      return;
    }
    const weeklyGoalMilestonesDataChild = await response.json();
    console.log(
      "Answer from BE of weekly goal milestone data from child",
      weeklyGoalMilestonesDataChild,
    );

    return weeklyGoalMilestonesDataChild;
  }

  //ENPOINT TO Get ONLY BOOKS READ we can put limit like -> http://127.0.0.1:8000/api/children/${child_id}/milestones?limit=1
  async function booksReadMilestonesPerChild(child_id) {
    if (!currentUser) return;

    const token = await currentUser.getIdToken();
    const response = await fetch(
      `http://127.0.0.1:8000/api/children/${child_id}/milestones?type=books_read`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );
    if (!response.ok) {
      console.error("Error getting books read milestones");
      return;
    }
    const booksReadMilestonesDataChild = await response.json();
    console.log(
      "Answer from BE of books read milestone data from child",
      booksReadMilestonesDataChild,
    );

    return booksReadMilestonesDataChild;
  }


    //ENPOINT TO Get Last WEEKLY GOAL from child to get one http://127.0.0.1:8000/api/children/${child_id}/milestones?limit=1
    //returns an array
  async function getSingleWeeklyGoal(child_id) {
    if (!currentUser) return;

    const token = await currentUser.getIdToken();
    // ADD TYPE = WEEKLY_GOAL to only receive 
    const response = await fetch(
      `http://127.0.0.1:8000/api/children/${child_id}/milestones?limit=1&type=weekly_goal`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );
    if (!response.ok) {
      console.error("Error getting single weekly");
      return;
    }
    const singleWeeklyGoal = await response.json();
    console.log(
      "Answer from BE of single weekly goal",
      singleWeeklyGoal,
    );

    return singleWeeklyGoal;
  }

      //ENPOINT TO Get Last MILESTONE (BOOKS_READ) from child to get one http://127.0.0.1:8000/api/children/${child_id}/milestones?limit=1
    //returns an array
  async function getSingleMilestone(child_id) {
    if (!currentUser) return;

    const token = await currentUser.getIdToken();
    // ADD TYPE = BOOKS_READ to only receive books milestone
    const response = await fetch(
      `http://127.0.0.1:8000/api/children/${child_id}/milestones?limit=1&type=books_read`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );
    if (!response.ok) {
      console.error("Error getting single milestone");
      return;
    }
    const singleMilestone = await response.json();
    console.log("Answer from BE of single milestone", singleMilestone);

    return singleMilestone;
  }

  return (
    <MilestonesContext.Provider
      value={{
        completeWeeklyMilestone,
        allMilestonesPerChild,
        weeklyGoalMilestonesPerChild,
        booksReadMilestonesPerChild,
        getSingleWeeklyGoal,
        getSingleMilestone,
      }}
    >
      {children}
    </MilestonesContext.Provider>
  );
}
