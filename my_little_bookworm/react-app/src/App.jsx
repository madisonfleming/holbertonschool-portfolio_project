import Login from "./components/auth/login";
import Header from "./components/header";
import Dashboard from "./components/dashboard";
import Home from "./components/home";

import { AuthProvider } from "./contexts/AuthContext";
//function of react to a list of routes into elements react, browser create the navigation system and navigate only tells where
import { BrowserRouter, useRoutes } from "react-router-dom";

function AppRoutes() {
  const routesArray = [
    { path: "/", element: <Home /> },
    { path: "*", element: <Home /> },
    { path: "/login", element: <Login /> },
    { path: "/dashboard", element: <Dashboard /> },
    { path: "/home", element: <Home /> },
  ];

  return useRoutes(routesArray);
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Header />
          <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;