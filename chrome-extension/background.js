console.log("Shield extension is running.");
const TESTING = true; // change to false before publishing
const sec_10 = 10000 //sec

// --- WEBSITE BLOCKER ---
// Your blocking rules are automatically handled by "rules.json"
// Nothing needed here unless you want to modify rules dynamically

// --- HISTORY SENDER ---

let CHILD_ID = null;  // Initialize CHILD_ID as null
let PARENT_ID = 69538921;  // Initialize PARENT_ID as null
let CHILD_NUMBER = 1; // Initialize CHILD_NUMBER
let SERVER_URL = "http://127.0.0.1:8000";  // Initialize SERVER_URL as null

// Function to fetch the Parent ID, Child Number, and Server URL from storage
function getParentIdChildNumberAndServerUrl() {
    return new Promise((resolve, reject) => {
        chrome.storage.local.get(['parentId', 'childNumber', 'serverUrl'], function(result) {
            if (chrome.runtime.lastError) {
                reject(chrome.runtime.lastError);
            } else {
                resolve({
                    parentId: result.parentId,
                    childNumber: result.childNumber,
                    serverUrl: result.serverUrl
                });
            }
        });
    });
}

// Function to fetch the Child ID based on Parent ID and Child Number
async function fetchChildId() {
    try {
        const { parentId, childNumber, serverUrl } = await getParentIdChildNumberAndServerUrl();  // Get Parent ID, Child Number, and Server URL from storage

        if (!parentId || !childNumber || !serverUrl) {
            console.error('Parent ID, Child Number, or Server URL is not set.');
            return;
        }

        PARENT_ID = parentId;
        CHILD_NUMBER = childNumber;
        SERVER_URL = serverUrl;

        // Fetch the Child ID from the server based on Parent ID and Child Number
        const response = await fetch(`${SERVER_URL}/api/get-child-id/?parent_id=${PARENT_ID}&child_number=${CHILD_NUMBER}`);
        const data = await response.json();
        CHILD_ID = data.child_id;  // Save the Child ID
        console.log('Fetched Child ID:', CHILD_ID);
    } catch (error) {
        console.error('Failed to fetch Child ID:', error);
    }
}

// Function to fetch history and send to server
async function sendHistory() {
    // Wait for the Child ID to be fetched before proceeding
    if (!CHILD_ID || !SERVER_URL) {
        console.log('Child ID or Server URL is not available yet.');
        return;
    }

    chrome.history.search({ text: '', maxResults: 20 }, async function(historyItems) {
        console.log('Fetched history:', historyItems);

        try {
            const response = await fetch(`${SERVER_URL}/api/upload_history/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    child_id: String(CHILD_ID),  // Make sure this is in the string format
                    history: historyItems
                })
            });

            console.log('Request sent:', {
                child_id: CHILD_ID,
                history: historyItems
            });

            // Log the response from the API
            console.log('API response status:', response.status);
            if (response.ok) {
                console.log('Request succeeded');
            } else {
                console.log('Request failed', await response.text());
            }

            const data = await response.json();
            console.log('Server response:', data);
        } catch (error) {
            console.error('Failed to send history:', error);
        }
    });
}

// On install, fetch Child ID and set alarm
chrome.runtime.onInstalled.addListener(() => {
    console.log('Extension installed, fetching Child ID and setting up history sending alarm.');

    chrome.storage.local.set({
      parentId: 69538921,        // your default parent ID
      childNumber: 1,            // your default child number
      serverUrl: "http://127.0.0.1:8000"  // your Django server URL
  }, function() {
      console.log('Initial data is set in storage.');
  });
    // Fetch the Child ID once the extension is installed
    fetchChildId().then(() => {
        if (TESTING) {
            // For testing, every 10 seconds
            setInterval(() => {
                console.log('Testing mode: Sending history every 10 seconds...');
                sendHistory();
            }, 10000);
        } else {
            // Production: create alarm every 5 minutes

              setInterval(() => {
                console.log('Testing mode: Sending history every 10 seconds...');
                sendHistory();
            }, sec_10*2);

            // console.log('Production mode: setting alarm every 5 minutes.');
            // chrome.alarms.create('sendHistoryAlarm', { periodInMinutes: 1 });
            // sendHistory(); // Also send once immediately
        }

    });
});

// On alarm trigger
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'sendHistoryAlarm') {
      console.log('Alarm triggered: sending history...');
      sendHistory();
  }
});

