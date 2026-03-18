import Container2 from "../../components/home/Container2";
import "./home.css";
import Cont1 from "../../components/home/Cont1";
import Cont3 from "../../components/home/Cont3";

export default function Home() {
  console.log("Home is rendering");
  return (
    <div className="home-grid">
      <div className="container1">
        <Cont1 />
      </div>
      <div className="container2"></div>
      <Container2 />
    <Container2 />
    <div className="container3">
      <div className="container3-top">
        <div className="container3-top-left">
        <p>
          Download a Certificate after
          completing a Milestone or Reward
          that you<br /> and your child can hold
          onto forever  
        </p>
        <p>
          (if you get a star, don't forget to
          cut and colour with your wormie!)
        </p>
        </div>
        <div className="container3-top-right">
        <img src={"/certificates.png"} className="certificates" />
        </div>
      </div>
      <div className="container3-bottom">
      <div className="container3-bottom-left">
        <img src={"/worm-gradient.svg"} className="worm-gradient" /> {/* worm image on bottom left */}
      </div>
      <div className="container3-bottom-right">
        <p>Track your wormies progress<br /> toward the 1,000 book goal</p>
      </div>
      </div>
    </div>

    </div>
  );
}
