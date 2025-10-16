import React, { useState } from "react";

function Content() {
  const [activeTab, setActiveTab] = useState("email");

  return (
    <div className="ful2">
      <h2>SafeSurf Detects and Monitors Phishing and Scam Sites</h2>
      <p>With SafeSurf, you can scan suspicious URLs and emails.</p>
      <ul className="tabs">
        <li 
          className={activeTab === "email" ? "active tab" : "tab"}
          onClick={() => setActiveTab("email")}
        >
          Email
        </li>
        <li 
          className={activeTab === "url" ? "active tab" : "tab"}
          onClick={() => setActiveTab("url")}
        >
          URL
        </li>
      </ul>
      <div className="tab-content">
        {activeTab === "email" && (
          <div>
            <h3>Email</h3>
            <input type="email" placeholder="example@gmail.com" />
            <button>Scan</button>
            <p>
              SafeSurf scans and checks the email you provide for threats.
            </p>
          </div>
        )}
        {activeTab === "url" && (
          <div>
            <h3>URL</h3>
            <input type="url" placeholder="https://example.com" />
            <button>Scan</button>
            <p>
              SafeSurf scans and checks the URL you provide for threats.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Content;
