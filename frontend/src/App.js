import React from "react";
import Header from "./components/header";
import Warning from "./components/warning";
import Content from "./components/content";
import Footer from "./components/footer";
import './style.css';

function App() {
  return (
    <div className="App">
      <Header />
      <Warning />
      <Content />
      <Footer />
    </div>
  );
}

export default App;
