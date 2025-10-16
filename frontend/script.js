document.addEventListener('DOMContentLoaded', function () {
    // URL Analysis
    const urlButton = document.getElementsByClassName('scn-url')[0]; // Get the first button with this class
    if (urlButton) {
        urlButton.addEventListener('click', async function(event) {
            event.preventDefault();
            const url = document.querySelector('input[name="URLs"]').value;

            // Validate URL input
            if (!url) {
                alert('Please enter a URL');
                return;
            }

            // Show loading spinner
            const loadingSpinner = document.getElementById('loading');
            if (loadingSpinner) loadingSpinner.style.display = 'block';

            try {
                const response = await fetch('http://127.0.0.1:5000/analyze_url', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ url: url })
                });

                const data = await response.json();

                // Hide loading spinner after request is complete
                if (loadingSpinner) loadingSpinner.style.display = 'none';

                // Handle errors in response
                if (data.error) {
                    alert(`Error: ${data.error}`);
                } else {
                    // Save the result to localStorage
                    localStorage.setItem('urlResult', JSON.stringify({
                        url: url,
                        result: data.result
                    }));
                }

                // Redirect to result page
                window.location.href = 'result-url.html';
            } catch (error) {
                // Hide loading spinner if an error occurs
                if (loadingSpinner) loadingSpinner.style.display = 'none';
                console.error(error);
                alert('Error checking the URL');
            }
        });
    } else {
        console.error('URL button not found');
    }

    // Email Analysis
    const emailButton = document.getElementsByClassName('scn-email')[0]; // Get the first button with this class
    if (emailButton) {
        emailButton.addEventListener('click', async function(event) {
            event.preventDefault();
            const email = document.querySelector('input[name="E-mail"]').value;
            const password = document.querySelector('input[name="password"]').value;
            const folder = document.querySelector('input[name="folder"]').value;

            // Validate Email, Password, and Folder input
            if (!email || !password || !folder) {
                alert('Please provide all required fields (email, password, folder)');
                return;
            }

            // Validate Folder name (either 'inbox' or 'spam')
            const folderName = folder.toLowerCase();
            if (folderName !== 'inbox' && folderName !== 'spam') {
                alert('Invalid folder name. Please select either "inbox" or "spam".');
                return;
            }

            // Show loading spinner
            const loadingSpinner = document.getElementById('loading');
            if (loadingSpinner) loadingSpinner.style.display = 'block';

            try {
                const response = await fetch('http://localhost:5000/analyze_email', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email: email, password: password, folder: folder })
                });

                const data = await response.json();

                // Hide loading spinner after request is complete
                if (loadingSpinner) loadingSpinner.style.display = 'none';

                // Handle errors in response
                if (data.error) {
                    alert(`Error: ${data.error}`);
                } else {
                    // Save the result to localStorage
                    localStorage.setItem('emailResult', JSON.stringify(data));
                }

                // Redirect to result page
                window.location.href = 'result-email.html';
            } catch (error) {
                // Hide loading spinner if an error occurs
                if (loadingSpinner) loadingSpinner.style.display = 'none';
                console.error(error);
                alert('Error analyzing the email');
            }
        });
    } else {
        console.error('Email button not found');
    }
});
