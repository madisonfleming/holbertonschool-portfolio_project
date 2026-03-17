import { Link } from "react-router-dom";
import MyNavbar from "../../components/navbar";
import "./header.css";

const Header = () => {
  console.log("Home rendering");
  return (
    <div className="header">
      <div className="logo">
        <img src={`logo.svg`} className="logo-img" />
      </div>
      <div>
        <MyNavbar className="navbar" />
      </div>
    </div>
  );
};

export default Header;
