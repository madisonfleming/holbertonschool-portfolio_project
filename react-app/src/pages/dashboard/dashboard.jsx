import { useEffect, useState } from "react";
import { useAuth } from "../../contexts/AuthContext";
import WeeklyGoal from "../../components/dashboard/WeeklyGoal";
import { getWeeklyTheme } from "../../utils/GetWeeklyTheme";
import "./dashboard.css";
import Milestones from "../../components/dashboard/Milestones";
import AddReadingSession from "../../components/dashboard/AddReadingSession";
import ChildList from "../../components/dashboard/ChildList";
import CreateChild from "../../components/dashboard/CreateChild";

const Dashboard = () => {
  const [children, setChildren] = useState([]);
  const { currentUser } = useAuth();
  const theme = getWeeklyTheme();
  const [buttonAddReadingSessionPopup, setButtonAddReadingSessionPopup] =
    useState(false);
  const [buttonCreateChildPopup, setButtonCreateChildPopup] = useState(false);

  const current_num_of_books = 100; // vendrá del backend
  const target = 1000; // vendrá del backend

  //ENDPOINT
  async function loadData() {
    if (!currentUser) return;
    const token = await currentUser.getIdToken();
    console.log("Token:", token);
    //need to do fetch to an endpoint that use that function
    const response = await fetch("http://127.0.0.1:8000/api/protected", {
      //firebase do the login -> generate the JWT
      //On HBNB was a POST because the login was manage by the back end but in here the login is manage by firebase so is GET the BE just return data
      headers: {
        //sending the token to the backend so fastapi receive it as a credential
        Authorization: `Bearer ${token}`,
      },
    });
    //geting the decoded token from the backend
    const data = await response.json();
    console.log("this is data from api/protected:", data);

    //FETCH TO GET ALL CHILDREN
    const childrenRes = await fetch("http://127.0.0.1:8000/api/children", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const childrenData = await childrenRes.json();

    // Adjust data fro the use of frontend
    const formatted = childrenData.map((child) => ({
      id: child.id,
      name: child.name,
      age: child.age,
      avatar: child.avatar_url,
    }));

    setChildren(formatted);
  }

  //FETCH TO ENDPOINT TO CREATE A CHILD
  async function createChild(childData) {
    if (!currentUser) return;

    const token = await currentUser.getIdToken();

    const response = await fetch("http://127.0.0.1:8000/api/children", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`, // NECESARIO
      },
      body: JSON.stringify(childData),
    });

    if (!response.ok) {
      console.error("Error creating child");
      return;
    }

    const newChild = await response.json();
    console.log("Answer from BE:", newChild);

    // UPDATE UI INMEDIATLY
    setChildren((prev) => [
      ...prev,
      {
        id: newChild.id,
        name: newChild.name,
        date_of_birth: newChild.date_of_birth,
        avatar_url: newChild.avatar_url,
      },
    ]);
  }

  //to validate the existance of user useEffect detecs the change of currentUser from null to login
  useEffect(() => {
    loadData();
  }, [currentUser]);

  return (
    <div>
      <div className="reading-session-container">
        <img
          src={`open-book.png`}
          className="open-book-img"
          onClick={() => setButtonAddReadingSessionPopup(true)}
          type="button"
        />
        <p className="reading-text">Add Reading Session</p>
      </div>
      <h1 className="dashboard-title">Let's get reading, wormies!</h1>
      <AddReadingSession
        trigger={buttonAddReadingSessionPopup}
        setTrigger={setButtonAddReadingSessionPopup}
        children_RS={children}
      ></AddReadingSession>
      <div className="dashboard-grid">
        <div className="children-container">
          <ChildList childrenData={children} />
          {/* createChild buttom */}
          <div className="create-child-container">
            <button
              className="complete-btn"
              onClick={() => setButtonCreateChildPopup(true)}
            >
              Create Child
            </button>
          </div>
          {/* For pop up the create child card  need to be outside so the weekly goal text doesnt appear infront */}
          {/*FE send to the BE a POST with this json */}
          <CreateChild
            trigger={buttonCreateChildPopup}
            setTrigger={setButtonCreateChildPopup}
            createChild={createChild}
          ></CreateChild>
        </div>
        <div className="weekly-container">
          <WeeklyGoal
            current_num_of_books={current_num_of_books}
            target={target}
            theme={theme}
          />
        </div>
        {/* 
        <div className="milestones-container">
          <Milestones current_num_of_books={current_num_of_books} target={target} />
        </div>
        */}
      </div>
    </div>
  );
};

export default Dashboard;
