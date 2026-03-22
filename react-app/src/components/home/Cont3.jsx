import React from "react";
import "./Cont3.css";

const Cont3 = () => {
  return (
    <div className="Cont3">
      <div className="container3-top">
        <div className="container3-top-left">
          <p className="title">
            Download a Certificate after completing a Milestone or Reward that
            you
            <br /> and your child can hold onto forever
          </p>
          <p className="section-desc">
            (if you get a star, don't forget to cut and colour with your
            wormie!)
          </p>
        </div>
        <div className="container3-top-right">
          <img src={"/certificates.png"} className="certificates" />
        </div>
      </div>
      <div className="container3-bottom">
        <div className="container3-bottom-left">
          <img src={"/worm-gradient.svg"} className="worm-gradient" />{" "}
          {/* worm image on bottom left */}
        </div>
        <div className="container3-bottom-right">
          <p className="title">
            Track your wormies progress
            <br /> toward the 1,000 book goal
          </p>
        </div>
      </div>
    </div>
  );
};

export default Cont3;
