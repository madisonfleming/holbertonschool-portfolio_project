//this file create e global context and every component can have access using useChild the hook
import React, { useState, useEffect, useContext } from "react";
import { useAuth } from "./AuthContext";
//create a new context object with defalt value null
const ChildContext = React.createContext()

//a hook
export function useChild() {
    return useContext(ChildContext);
}

//child provider provides the child to all the children(are the components which provider wraps
export function ChildProvider({ children }) {

    const [childList, setChildList] = useState([]);
    const [selectedChild, setSelectedChild] = useState(null);
    //load the current state of the child
    const [loading, setLoading] = useState(true);
    const { currentUser } = useAuth();
    
    //to get all the children
    async function loadData() {
        try {
            const token = await currentUser.getIdToken();
            //to fetch the children
            const childrenRes = await fetch("http://127.0.0.1:8000/api/children", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            const childrenData = await childrenRes.json();
            console.log("this is children data", childrenData)

            // Ajustamos la data al formato que usa tu frontend
            const formatted = childrenData.map((child) => ({
                id: child.id,
                name: child.name,
                age: child.age,
                avatar: child.avatar_url,
            }));
            setChildList(formatted);
            //set selectedchild to default first child value im unsure if this should be deleted
            setSelectedChild(formatted[0]?.id);
            setLoading(false);
        } catch (error) {
            console.error("Error fetch child", error)
            setLoading(false);
        }
        
    }

     //FETCH TO ENDPOINT TO CREATE A CHILD
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
    console.log("Answer from BE of creating new child:", newChild);

    // UPDATE UI INMEDIATLY
    setChildList((prev) => [
      ...prev,
      {
        id: newChild.id,
        name: newChild.name,
        age: newChild.age,
        avatar: newChild.avatar,

      },
    ]);
  }

    //to validate the existance of child useEffect detects the change of child from null to fetched
    useEffect(() => {
    if (currentUser) loadData();
  }, [currentUser]);


    return (
        //children will have access to the value properties
        <ChildContext.Provider 
        value={{childList, 
        setChildList, 
        selectedChild, 
        setSelectedChild,
        createChild,
        }}>
            {!loading && children}
        </ChildContext.Provider>
    )

}
