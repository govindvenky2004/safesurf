import React, { useState } from 'react';

function PhishingCheckForm() {
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Handle form input change
  const handleChange = (event) => {
    setInput(event.target.value);
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);

    // Simulate an API call to check for phishing
    // Replace this with an actual API request to your backend
    setTimeout(() => {
      // Example result
      if (input.toLowerCase().includes('phish')) {
        setResult('This is a phishing URL/Email.');
      } else {
        setResult('This is a legitimate URL/Email.');
      }
      setIsLoading(false);
    }, 1500); // Simulate loading time
  };

  return (
    <div>
      <h2>Check URL or Email for Phishing</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={handleChange}
          placeholder="Enter URL or Email"
          required
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Checking...' : 'Check'}
        </button>
      </form>

      {result && (
        <div className="result">
          <p>{result}</p>
        </div>
      )}
    </div>
  );
}

export default PhishingCheckForm;
