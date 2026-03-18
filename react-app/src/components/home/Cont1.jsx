import React from "react";
import "./Cont1.css";

const Cont1 = () => {
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
            15 Minutes A Night Could Give Your Child A{" "}
            <em>Lifetime Of Confidence</em>
          </h2>
          <p className="section-desc">
            Kids who've read 1,000 books before kindergarten have dramatically
            better outcomes.
            <strong>My Little Bookworm</strong> makes tracking every book
            effortless — so you can focus on what matters: reading together.
          </p>
        </div>

        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon-wrap c1">
              <img src="/mlb-book.svg" />
            </div>
            <div className="feature-title">Track 1,000 Books</div>
            <div className="feature-desc">
              Every read counts — log books in seconds, never lose track
            </div>
          </div>

          <div className="feature-card">
            <div className="feature-icon-wrap c2">
              <img src="/themes/rocket.png" />
            </div>
            <div className="feature-title">Built For Busy Parents</div>
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
              Keep kids motivated with certificates and weekly goals
            </div>
          </div>

          <div className="feature-card">
            <div className="feature-icon-wrap c4">
              <img src="/mlb-star.png" />
            </div>
            <div className="feature-title">Research-Backed</div>
            <div className="feature-desc">
              1,000 books = better educational outcomes, proven by science
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cont1;
