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
      <div className="container2">
      <Container2 />
      <Container2 />
    </div>

    </div>
  );
}
