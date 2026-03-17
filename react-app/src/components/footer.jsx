import React from "react";
import './footer.css'
import { Link } from "react-router-dom";

const Footer = () => {

    return (
        <footer className="footer">
            <div className="footer-container">
                <div className="img" ></div>
                {/*<Link className="text">&copy; My Little Bookworm {new Date().getFullYear()}</Link>*/}
            </div>
        </footer>
    );
};

export default Footer;
