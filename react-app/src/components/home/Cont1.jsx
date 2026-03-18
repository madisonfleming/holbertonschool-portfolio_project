import React from "react";
import "./Cont1.css";
import { useNavigate } from "react-router-dom";

const Cont1 = () => {
  const navigate = useNavigate();
  return (
    <div className="cont1-body">
      <div className="section">
        <div className="section-header">
          <div className="stack">
            <div className="mini-worm">
              <img src="/mlb-fav.png" />
            </div>
            <div className="eyebrow">Trusted by 1,000+ families</div>
          </div>
          <h2 className="section-title">
            15 minutes a night could give your child a{" "}
            <em>lifetime of confidence</em>
          </h2>
          <p className="section-desc">
            Children who share 1,000 books with a parent or carer before
            kindergarten have dramatically better outcomes.
            <strong> My Little Bookworm</strong> makes tracking every book
            effortless, so you can focus on what matters: reading together.
          </p>
        </div>

        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon-wrap c1">
              <img src="/mlb-book.svg" />
            </div>
            <div className="feature-title">Track 1,000 Books</div>
            <div className="feature-desc">
              Every read counts! Log books in seconds, never lose track.
            </div>
          </div>

          <div className="feature-card">
            <div className="feature-icon-wrap c2">
              <img src="/themes/rocket.png" />
            </div>
            <div className="feature-title">Built for all families</div>
            <div className="feature-desc">
              Log books in seconds, stay on top of your child's progress
            </div>
          </div>

          <div className="feature-card">
            <div className="feature-icon-wrap c3">
              <img src="/mlb-trophy.png" />
            </div>
            <div className="feature-title">Rewards & Milestones</div>
            <div className="feature-desc">
              Keep children motivated with weekly goals and tangible
              certificates
            </div>
          </div>

          <div className="feature-card">
            <div className="feature-icon-wrap c4">
              <img src="/mlb-star.png" />
            </div>
            <div className="feature-title">Early-literacy research</div>
            <div className="feature-desc">
              Supports better educational outcomes
            </div>
          </div>
        </div>
        <div className="button-text-section">
          <button className="btn-login" onClick={() => navigate("/login")}>
            Start reading today
          </button>
          <p class="text-down-btn">Completely free! Join today</p>
        </div>
      </div>
    </div>
  );
};

export default Cont1;
