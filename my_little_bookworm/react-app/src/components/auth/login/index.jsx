import "./login.css"
import { useState } from "react";
import { auth } from "../../../firebase/firebase";
import { signInWithEmailAndPassword } from "firebase/auth";
import { googleProvider } from "../../../firebase/firebase";
import { signInWithPopup } from "firebase/auth";


function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      await signInWithEmailAndPassword(auth, email, password);
      setMessage("Login exitoso!");
    } catch (error) {
      setMessage("Error: " + error.message);
    }
  };

  //handle google login
  const handleGoogleLogin = async () => {
  try {
    await signInWithPopup(auth, googleProvider);
    setMessage("Login con Google exitoso!");
  } catch (error) {
    setMessage("Error: " + error.message);
  }
};


  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="title">My Little Bookworm</h1>
        <p className="subtitle">Welcome Back!</p>
        <p className="description">Log in to continue your reading journey</p>

        <form onSubmit={handleLogin}>
          <label>Email Address</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />

          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />

          <button className="primary-btn">Log In →</button>
        </form>

        <button className="google-btn" onClick={handleGoogleLogin}>
          Continue with Google
        </button>
      </div>
    </div>
  );
}

export default Login;