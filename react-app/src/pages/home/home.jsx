import Container2 from "../../components/home/Container2";
import "./home.css";

export default function Home() {
  console.log("Home is rendering");
  return (
    <div className="home-grid">
    <div className="container1"></div>
    <div className="container2">
      <Container2 />
    </div>
    <div className="container3"></div>
    </div>
  );
}
