import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { getAuth, signOut } from "firebase/auth"; // import functionality for logout from firebase SDK module
import './../App.css'

function MyNavbar() {
  const { currentUser } = useAuth();
  const navigate = useNavigate();
  const auth = getAuth();

  const handleLogout = async () => { // facilitates logging out of firebase
    await signOut(auth);
    navigate("/home"); // redirects user to home page after logout
  };

  return (
    <div>
      <Navbar expand="lg">
        <Container>
          <Navbar.Toggle
            className="navbar-toggle"
            aria-controls="basic-navbar-nav"
          />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto">
              <Nav.Link className="px-3" as={Link} to="/home">
                Home
              </Nav.Link>
              {!currentUser && (
                <Nav.Link className="px-3" as={Link} to="/login">
                  Login
                </Nav.Link>
              )}
              {currentUser && (
                <Nav.Link className="px-3" as={Link} to="/dashboard">
                  Dashboard
                </Nav.Link>
              )}
              {currentUser && (
                <Nav.Link className="px-3" as={Link} to="/child-profiles">
                  Child Profiles
                </Nav.Link>
              )}
              {currentUser && (
                <Nav.Link className="px-3" as={Link} to="/settings">
                  Settings
                </Nav.Link>
              )}
              {currentUser && (
                <Nav.Link className="px-3" onClick={handleLogout}>
                  Log Out
                </Nav.Link>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </div>
  );
}

export default MyNavbar;
