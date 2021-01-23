import 'bootstrap/dist/css/bootstrap.css';
import { BrowserRouter, Switch, Route, Redirect } from "react-router-dom";
import Register from "./Register.js"
import { useState } from 'react';
import Header from './Header';
import Login from "./Login.js"
import Home from "./Home.js"
import ImportLocations from "./ImportLocations.js"
import JoinFamily from "./JoinFamily.js"
import Activate from "./Activate.js"
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(localStorage.getItem("token") != null);

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
                return <JoinFamily token={props.match.params.token} />
              } else {
                return <Redirect to="/login"></Redirect>;
              }
            }}
          />
          <Route
            exact
            path="/exports/:id"
            render={(props) => {
              if (isLoggedIn) {
                return <ImportLocations id={props.match.params.id} />
              } else {
                return <Redirect to="/login"></Redirect>;
              }
            }}
          />
          <Route
            exact
            path="/activate/:token"
            render={(props) => {
              if (!isLoggedIn) {
                return <Activate token={props.match.params.token} />
              } else {
                return <Redirect to="/"></Redirect>;
              }
            }}
          />
        </Switch>
      </BrowserRouter>
    </div >
  );
}

export default App;
