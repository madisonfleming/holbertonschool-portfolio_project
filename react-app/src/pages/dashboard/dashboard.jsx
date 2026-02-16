import { useEffect, useState } from "react";
import { useAuth } from '../../contexts/AuthContext'
import WeeklyGoal from '../../components/dashboard/WeeklyGoal';
import { getWeeklyTheme } from "../../utils/GetWeeklyTheme";
import "./dashboard.css";
import Milestones from '../../components/dashboard/Milestones';
import AddReadingSession from "../../components/dashboard/AddReadingSession";

const Dashboard = () => {
  const { currentUser } = useAuth();
  const theme = getWeeklyTheme();
  const [buttonAddReadingSessionPopup, setButtonAddReadingSessionPopup] = useState(false);

  const current_num_of_books = 500;   // vendrá del backend
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
      <h1 className="dashboard-title">Let's get reading, wormies!</h1>
      <AddReadingSession trigger={buttonAddReadingSessionPopup} setTrigger={setButtonAddReadingSessionPopup}>
      </AddReadingSession>
      <div className="dashboard-container">
        <img src={`open-book.png`} className="open-book-img" />
        <button onClick={() => setButtonAddReadingSessionPopup(true)} type="button" class="btn btn-primary btn-sm">Add Reading Session</button>
        <WeeklyGoal current_num_of_books={current_num_of_books} target={target} theme={theme} />
        <Milestones current_num_of_books={current_num_of_books} target={target} />
      </div>

    </div>
  )
}

export default Dashboard

