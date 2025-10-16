import React from "react";

function Header() {
  return (
    <header className="hmt">
      <div className="menu">
        <label>
          <i className="fa fa-bars"></i>
        </label>
      </div>

      <ul className="btns">
        <li><a href="#">Home</a></li>
        <li><a href="#">Settings</a></li>
        <li><a href="#">About</a></li>
        <li><a href="#">Builders</a></li>
        <li>
          <a href="#"><i className="fab fa-facebook"></i></a>
          <a href="#"><i className="fab fa-twitter"></i></a>
          <a href="#"><i className="fab fa-instagram"></i></a>
        </li>
      </ul>

      <div className="search-box">
        <form>
          <input type="text" name="search" placeholder="Type to search" />
          <button type="submit"><i className="fa fa-search"></i></button>
        </form>
      </div>
    </header>
  );
}

export default Header;
