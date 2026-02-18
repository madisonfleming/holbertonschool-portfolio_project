import Login from './pages/login/login';
import Header from './pages/header/header';
import Dashboard from './pages/dashboard/dashboard';
import Home from './pages/home/home';
import ChildProfiles from './pages/child-profiles/child-profiles';

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
    { path: "/child-profiles", element: <ChildProfiles /> },
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
