import React from "react";
import './footer.css'
import { Link } from "react-router-dom";

const Footer = () => {

    return (
        <footer className="footer">
            <div className="footer-container">
                <p className="text">&copy; My Little Bookworm {new Date().getFullYear()}</p>
                <Link className="footer-links">About Us</Link>
                <Link className="footer-links">Contact Us</Link>
                </div>
        </footer>
    );
};

export default Footer;
