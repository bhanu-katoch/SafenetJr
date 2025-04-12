document.getElementById('saveButton').addEventListener('click', function() {
    const parentId = document.getElementById('parentId').value.trim();
    const childNumber = document.getElementById('childNumber').value.trim();

    if (parentId && childNumber) {
        // Save Parent ID and Child Number to local storage
        chrome.storage.local.set({ parentId: parentId, childNumber: childNumber }, function() {
            if (chrome.runtime.lastError) {
                alert("Error saving data: " + chrome.runtime.lastError);
            } else {
                alert("Configuration saved successfully!");
            }
        });
    } else {
        alert("Please fill both Parent ID and Child Number.");
    }
});
