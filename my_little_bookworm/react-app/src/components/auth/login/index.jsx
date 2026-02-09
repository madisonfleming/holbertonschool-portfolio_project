import "./login.css"
import { useState } from "react";
import { doSignInWithEmailAndPassword, doSignInWithGoogle } from "../../../firebase/auth";
import { useAuth } from "../../../contexts/AuthContext";
import { Navigate } from "react-router-dom";


const Login = () => {
  //to see the user status
  const { userLoggedIn } = useAuth();
  //this local states save what does the user writes
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSigningIn, setIsSigningIn] = useState(false);

  //when user log in we check if user is signing in 
  const onSubmit = async (e) => {
        e.preventDefault()
        if(!isSigningIn) {
            setIsSigningIn(true)
            await doSignInWithEmailAndPassword(email, password)
        }
    }

  const onGoogleSignIn = (e) => {
        e.preventDefault()
        if (!isSigningIn) {
            setIsSigningIn(true)
            //if there is a error the state var set to false
            doSignInWithGoogle().catch(err => {
                setIsSigningIn(false)
            })
        }
    }


  return (
    <div className="login-container">
      <div className="login-card">
       {userLoggedIn && (<Navigate to={'/dashboard'} replace={true} />)}
        <h1 className="title">My Little Bookworm</h1>
        <p className="subtitle">Welcome Back!</p>
        <p className="description">Log in to continue your reading journey</p>

        <form onSubmit={onSubmit}>
          <label>Email Address</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />

          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />

          <button className="primary-btn">Log In →</button>
        </form>

        <button className="google-btn" onClick={onGoogleSignIn}>
          Continue with Google
        </button>
        
      </div>
    </div>
  );
}

export default Login;