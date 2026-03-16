//this file create e global context and every component can have access using useChild the hook
import React, { useState, useEffect, useContext } from "react";
import { useAuth } from "./AuthContext";
//create a new context object with defalt value null
const ChildContext = React.createContext();

//a hook
export function useChild() {
  return useContext(ChildContext);
}

//child provider provides the child to all the children(are the components which provider wraps
export function ChildProvider({ children }) {
  const [childList, setChildList] = useState([]);
  const [selectedChild, setSelectedChild] = useState(null);
  //load the current state of the child
  //const [loading, setLoading] = useState(true);
  const { currentUser } = useAuth();

  //endpoint to get all the children
  async function loadData() {
    try {
      if (!currentUser) return;

      const token = await currentUser.getIdToken();
      //to fetch the children
      const childrenRes = await fetch("http://127.0.0.1:8000/api/children", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const childrenData = await childrenRes.json();
      console.log("this is children data", childrenData);

      // formatted data to use in FE
      // in the BE we received id, name, age, avatar_url
      const formatted = childrenData.map((child) => ({
        id: child.id,
        name: child.name,
        age: child.age,
        avatar: child.avatar_url,
      }));
      setChildList(formatted);
      //set selectedchild to default first child value im unsure if this should be deleted
      if (!selectedChild && formatted.length > 0) {
        setSelectedChild(formatted[0]);
      }

      //setLoading(false);
    } catch (error) {
      console.error("Error fetch child", error);
      //setLoading(false);
    }
  }

  //ENDPOINT TO CREATE A CHILD
  async function createChild(childData) {
    if (!currentUser) return;

    const token = await currentUser.getIdToken();

    const response = await fetch("http://127.0.0.1:8000/api/children", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(childData),
    });
    if (!response.ok) {
      console.error("Error creating child");
      return;
    }
    const newChild = await response.json();
    // we received id, name, age, avatar_url
    console.log("Answer from BE of creating new child:", newChild);
    // UPDATE UI INMEDIATLY
    setChildList((prev) => [
      ...prev,
      {
        id: newChild.id,
        name: newChild.name,
        age: newChild.age,
        avatar: newChild.avatar_url,
      },
    ]);
  }

  //UPDATE CHILD
  async function updateChild(id, updatedData) {
    console.log("PUT payload:", updatedData);

    if (!currentUser) return;

    const token = await currentUser.getIdToken();

    const response = await fetch(`http://127.0.0.1:8000/api/children/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(updatedData),
    });

    if (!response.ok) {
      console.error("Error updating child");
      return;
    }

    const updatedChild = await response.json();
    console.log("Answer from BE of updating a child:", updatedChild);
    // Update local state
    setChildList((prev) => {
      const updatedList = prev.map((child) => {
        if (child.id === id) {
          // search the child we want to update
          //... means copy all the properties into the new obj
          return {
            ...child,
            ...updatedChild,
            //this means if updated... has a valid url use it otherwise use child.avatar
            avatar: updatedChild.avatar_url ?? child.avatar,
          };
        } else {
          // if new data is not send stay with the old data
          return child;
        }
      });

      return updatedList;
    });
  }

  //to validate the existance of child useEffect detects the change of child from null to fetched
  useEffect(() => {
    if (currentUser) loadData();
  }, [currentUser]);

  return (
    //children will have access to the value properties
    <ChildContext.Provider
      value={{
        childList,
        setChildList,
        selectedChild,
        setSelectedChild,
        createChild,
        updateChild,
      }}
    >
      {children}
    </ChildContext.Provider>
  );
}
