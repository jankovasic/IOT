const firebaseConfig = {
    authDomain: "rpi1-5529c.firebaseapp.com",
    databaseURL: "https://rpi1-5529c-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "rpi1-5529c",
    storageBucket: "rpi1-5529c.appspot.com",
    messagingSenderId: "1036387295039",
    appId: "1:1036387295039:web:33465361e68ffe7c11bd8a",
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const database = firebase.database();

function fetchData() {
    const ref = database.ref("baza");
    // Listen for new data at the last entry in the database
    ref.limitToLast(1).on('value', function(snapshot) {
        // Since we're using limitToLast, we expect the snapshot to have only the latest entry.
        snapshot.forEach(function(childSnapshot) {
            const data = childSnapshot.val();
            console.log("Received data:", data);
            // Update display with the new data
            updateDisplay(data);
            if (data && data.gas_concentration > 600) {
                sendNotification();}
        });
    }, function(error) {
        console.error("Error fetching data", error);
        // Display error message or indication when an error occurs
        updateDisplay();
    });
}
function sendNotification() {
    alert("Detektovan je požar! Evakuišite se iz objekta!");
}

function updateDisplay(data) {
    // Retrieve the elements where data needs to be displayed
    const sensor_value = document.getElementById('sensor_value');

    if (data && data.gas_concentration != null) {
        if (data.gas_concentration != null) {
            // Update the text content of the elements with the new data, formatted to two decimals
            sensor_value.textContent = `${data.gas_concentration}`;
        } else {
            // Display a default message when gas data is unavailable
            sensor_value.textContent = "Gas data unavailable";
        }
   } else {
        // Display a default message when data is unavailable or not in the expected format
       sensor_value.textContent = "Data unavailable";
    }
}

function registerDevice() {
    const deviceIdInput = document.getElementById('device_id');
    const deviceId = deviceIdInput.value.trim();

    if (deviceId) {
        const devicesRef = database.ref('devices');
        devicesRef.child(deviceId).set({
            registered: true,
            lastActive: firebase.database.ServerValue.TIMESTAMP
        }, function(error) {
            if (error) {
                console.error("Error registering device:", error);
                alert("Failed to register device. Please try again.");
            } else {
                console.log("Device registered successfully.");
                alert("Device registered successfully.");
                deviceIdInput.value = "";  // Clear the input field after successful registration
            }
        });
    } else {
        alert("Please enter a valid device ID.");
    }
}

// Initialize data fetching when the window loads
window.onload = function() {
    fetchData();
};
