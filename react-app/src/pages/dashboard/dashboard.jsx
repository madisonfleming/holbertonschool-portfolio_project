import { useEffect, useState } from "react";
import { useAuth } from '../../contexts/AuthContext'
import WeeklyGoal from '../../components/dashboard/WeeklyGoal';
import { getWeeklyTheme } from "../../utils/GetWeeklyTheme";
import "./dashboard.css";
import Milestones from '../../components/dashboard/Milestones';
import AddReadingSession from "../../components/dashboard/AddReadingSession";
import ChildList from "../../components/dashboard/ChildList";


const Dashboard = () => {
  const children = [
    { id: 1, name: 'Billie', age: 3, avatar: "/star.svg", lastReadBook: "My Little Pony" },
    { id: 2, name: 'Hannah', age: 3, avatar: "/star.svg", lastReadBook: "My Little Bookworm" },
    { id: 4, name: 'Gia', age: 3, avatar: "/star.svg", lastReadBook: "My Little Kitten" },
  ];
  const { currentUser } = useAuth();
  const theme = getWeeklyTheme();
  const [buttonAddReadingSessionPopup, setButtonAddReadingSessionPopup] = useState(false);

  const current_num_of_books = 100;   // vendrá del backend
  const target = 1000;    // vendrá del backend

  //
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
        "Authorization": `Bearer ${token}`
      }
    });
    //geting the decoded token from the backend
    const data = await response.json();
    console.log("this is data:", data);
  };
  //to validate the existance of user useEffect detecs the change of currentUser from null to login
  useEffect(() => {
    loadData();
  }, [currentUser]);

  return (

    <div>
      <div className="reading-session-container">
        <img src={`open-book.png`} className="open-book-img" onClick={() => setButtonAddReadingSessionPopup(true)} type="button" />
        <p className="reading-text">Add Reading Session</p>
      </div>
      <h1 className="dashboard-title">Let's get reading, wormies!</h1>
      <AddReadingSession trigger={buttonAddReadingSessionPopup} setTrigger={setButtonAddReadingSessionPopup} children_RS={children}>
      </AddReadingSession>
      <div className="dashboard-grid">
        <div className="children-container">
          <ChildList child_list={children} />
        </div>
        <div className="weekly-container">
          <WeeklyGoal current_num_of_books={current_num_of_books} target={target} theme={theme} />
        </div>
        <div className="milestones-container">
          <Milestones current_num_of_books={current_num_of_books} target={target} />
        </div>
      </div>

    </div>
  )
}

export default Dashboard

