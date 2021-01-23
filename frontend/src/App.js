import 'bootstrap/dist/css/bootstrap.css';
import { BrowserRouter, Switch, Route, Redirect, useHistory } from "react-router-dom";
import Register from "./Register.js"
import { useState } from 'react';
import Header from './Header';
import Login from "./Login.js"
import Home from "./Home.js"
import axios from "axios"
import './App.css';

const join = (token) => {
  axios
    .get(`http://localhost:5000/api/families/join/${token}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
    .then((res) => {
    })
    .catch((e) => {
      alert("Cannot join family")
    });
}

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(localStorage.getItem("token") != null);
  const history = useHistory();

  return (
    <div className="app">
      <BrowserRouter>

        <Header />
        <Switch>
          <Route
            exact
            path="/register"
            render={() => {
              return <Register />;
            }}
          />
          <Route
            exact
            path="/login"
            render={() => {
              if (!isLoggedIn) {
                return <Login setIsLoggedIn={setIsLoggedIn} />;
              } else {
                return <Redirect to="/"></Redirect>;
              }
            }}
          />
          <Route
            exact
            path="/"
            render={() => {
              if (isLoggedIn) {
                return <Home />;
              } else {
                return <Redirect to="/login"></Redirect>;
              }
            }}
          />
          <Route
            exact
            path="/families/join/:token"
            render={(props) => {
              if (isLoggedIn) {
                join(props.match.params.token)
                return <Redirect to="/"></Redirect>;
              } else {
                return <Redirect to="/login"></Redirect>;
              }
            }}
          />
        </Switch>
      </BrowserRouter>
    </div >
  );
}

export default App;
