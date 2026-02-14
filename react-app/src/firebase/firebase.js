
// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyATSl59VVvIcoR_p_QgUpH6ZrnjbVXXb9c",
  authDomain: "mylittlebookworm-fde51.firebaseapp.com",
  projectId: "mylittlebookworm-fde51",
  storageBucket: "mylittlebookworm-fde51.firebasestorage.app",
  messagingSenderId: "305359697118",
  appId: "1:305359697118:web:556d3c5653bcf2c486be4f",
  measurementId: "G-MW2HC989GQ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
