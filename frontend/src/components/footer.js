import React from "react";

function Footer() {
  return (
    <footer className="ftr">
      <div className="cmp">
        <h3>Company</h3>
        <p>
          Developed by:<br />
          Amruth M, Amogh Siddarth, Govind Venkatesh, Hemanth M.
        </p>
      </div>

      <div className="prd">
        <h3>Quick Links</h3>
        <ul>
          <li><a href="#">Home</a></li>
          <li><a href="#">Settings</a></li>
          <li><a href="#">About</a></li>
          <li><a href="#">Builders</a></li>
        </ul>
      </div>

      <div className="cts">
        <h3>Contact Us</h3>
        <p>Ph.no: +91 8296734315</p>
      </div>
    </footer>
  );
}

export default Footer;
