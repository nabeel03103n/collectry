// Assuming this is executed in a Node.js or browser environment where fetch and DOM manipulation are available.

let url = "http://emitrauat.rajasthan.gov.in/webServicesRepositoryUat/getKioskDetailsJSON";

let users = []; // Get users from your database, this should be fetched dynamically based on your backend framework

// For demonstration, assuming this array is populated with user data
users.push({ merchantID: "exampleMerchantID", SSOID: "exampleSSOID" });

users.forEach(user => {
    console.log(`Merchant ID: ${user.merchantID}\nSSOID: ${user.SSOID}`);

    let payload = new URLSearchParams({
        "MERCHANTCODE": user.merchantID,
        "SSOID": user.SSOID
    });

    let headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    };

    // Assuming you're inside an async function or handling promise properly
    fetch(url, {
        method: "POST",
        body: payload,
        headers: headers
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            console.log("Failed to get a response");
            console.log("Status code:", response.status);
            return { error: "Error 404 please contact your admin" };
        }
    })
    .then(data => {
        if (data.error) {
            console.log(data.error);
        } else {
            let arguments = Object.entries(data);
            let text = { "t1": arguments };
            console.log(text); // Do something with the text object
        }
    })
    .catch(error => {
        console.error("Request failed", error);
    });
});

// Function to handle form submission and saving data
function handleFormSubmission(event) {
    event.preventDefault(); // Prevent page reload on form submission

    let merchantID = document.querySelector('input[name="merchantID"]').value;
    let SSOID = document.querySelector('input[name="SSOID"]').value;

    if (merchantID && SSOID) {
        // Simulate saving to the backend (in a real app, you'd make a POST request here)
        console.log("Saving user:", { merchantID, SSOID });

        // After saving, you can also trigger your fetch call here as well
    } else {
        console.log("Failed to Fetch the details");
    }
}

// Attach the function to a form submit event in case of front-end usage
document.querySelector('form').addEventListener('submit', handleFormSubmission);
