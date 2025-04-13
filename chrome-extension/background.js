chrome.runtime.onInstalled.addListener(() => {
    // Define the API URL
    const parentId = '69538921';  //  parent ID
    const childNumber = 1;  //  child number

    const apiUrl = `http://127.0.0.1:8000/api/get-child-id/?parent_id=${parentId}&child_number=${childNumber}`;

    
  
    // Fetch data from the API
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        // Assuming the API returns a child ID, set it in local storage
        const childId = data.child_id;  // Adjust this if the API returns a different key
        
        // Store the child ID in Chrome's local storage
        chrome.storage.local.set({ childId: childId }, () => {
          console.log('Child ID stored:', childId);
        });
      })
      .catch(error => {
        console.error('Error fetching child ID:', error);
      });
  });

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.url) {
    // Get the child ID from chrome storage
    chrome.storage.local.get(['childId'], (result) => {
      const childId = result.childId;  // Retrieve the stored child ID

      // If the childId exists
      if (childId) {
        const visitedUrl = tab.url;  // Current tab URL
        const title = tab.title || "Untitled";  // Tab title, default to "Untitled"
        const visitTime = new Date().getTime();  // Current time in milliseconds

        const data = {
          child_id: childId,
          visited_url: visitedUrl,
          title: title,
          visit_time: visitTime
        };

        // API call to send data
        fetch('http://localhost:8000/api/upload_history/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        })
          .then(response => response.json())
          .then(data => console.log('Success:', data))
          .catch((error) => console.error('Error:', error));      
      } else {
        console.error("Child ID is not available.");
      }
    });
  }
});
