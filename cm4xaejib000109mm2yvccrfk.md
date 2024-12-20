---
title: "Building a Chrome Extension from Scratch"
seoTitle: "Create a Chrome Extension: Auto-Fill Author Details in Microsoft CMT"
seoDescription: "Learn step-by-step how to build a Chrome extension to auto-fill author details in Microsoft CMT. Save time and reduce manual effort with this powerful tool."
datePublished: Fri Dec 20 2024 21:53:17 GMT+0000 (Coordinated Universal Time)
cuid: cm4xaejib000109mm2yvccrfk
slug: building-a-chrome-extension-from-scratch
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1734731114331/723c2dd4-5d8b-4900-9e40-12a990749ce9.jpeg
tags: jquery, javascript, chrome-extension

---

Creating a Chrome extension can feel complex initially, but it becomes simpler when broken into pieces. Chrome extensions are zipped bundles of web technology files such as **HTML**, **CSS**, **JavaScript**, images, and a mandatory `manifest.json` file. These files work together to customize and enhance the browsing experience.

Extensions can:

* Modify web content or browser behavior.
    
* Add new UI elements like buttons or tooltips.
    
* Interact with web pages dynamically.
    

Essentially, a Chrome extension transforms your browser into a personalized tool for productivity, entertainment, or automation.

# How Do Extensions Work?

The structure and flow of a Chrome extension follow a modular architecture:

1. **Manifest File (**`manifest.json`):
    
    * The backbone of an extension.
        
    * Declares metadata like the extension's name, version, description, and permissions.
        
    
    Example snippet:
    
    ```json
    {
      "name": "My Extension",
      "version": "1.0",
      "description": "An example Chrome Extension",
      "permissions": ["tabs"],
      "background": {
        "scripts": ["background.js"]
      }
    }
    ```
    
2. **Core Components**: Chrome extensions typically consist of:
    
    * **Background Script**: Manages events and handles tasks silently in the background.
        
    * **Content Script**: Injected into web pages, enabling interaction with the page's DOM.
        
    * **UI Elements**: These include popups, toolbar icons, or options pages that users directly interact with.
        
3. **Communication Flow**:
    
    * Components communicate via messages to share data and actions (as shown in the attached image).
        
    * The image illustrates how different parts (e.g., `background.js`, `popup.js`, `content script.js`) exchange information and interact.
        

# Architecture overview

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1734728993176/08175dd8-f775-43a9-9547-517249086537.png align="center")

1. **Popup and Background Interaction**:
    
    * The user interacts with the **popup.html** UI through the browser toolbar.
        
    * The **popup.js** handles UI logic, often communicating with the **background.js** for event handling or data retrieval.
        
2. **Content Script Integration**:
    
    * **contentscript.js** operates within the web page context, enabling actions like auto-filling forms or altering the page's content.
        
    * This script communicates with the **background.js** or **popup.js** to fetch or send data.
        
3. **Message Flow**:
    
    * Each script sends messages (represented by arrows) to perform specific actions.
        
    * For example, **popup.js** might request the **background.js** to fetch stored data or trigger a task.
        

For full source code and updates, visit the official repository on GitHub:  
[**CMT Author Auto-Fill Chrome Extension**](https://github.com/arya2004/cmt-autofill/). Explore the implementation, contribute, or fork the project for your needs!

# Overview of Repository Structure

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1734729584150/41effd4b-d042-4870-a1d6-493004321352.png align="center")

Each file in the structure serves a specific purpose:

* `contentScript.js`: Injects custom scripts into the target web page to perform auto-fill operations.
    
* `jquery-3.7.1.min.js`: A lightweight, powerful JavaScript library used to simplify DOM manipulation.
    
* `popup.css`: Contains styling for the extension popup.
    
* `popup.html`: The HTML for the extension popup interface.
    
* `popup.js`: Implements the functionality for the popup interface, such as saving and loading author data.
    
* `manifest.json`: The core configuration file of the extension that defines permissions, scripts, and other key details.
    

## Generating the Repository Structure with a Bash Script

You can use the following Bash script to create this directory structure and download the required jQuery file automatically:

```bash
#!/bin/bash

# Create the directory structure
mkdir -p CMT-AUTOFILL/extension

touch CMT-AUTOFILL/manifest.json

# Navigate to the extension directory
cd CMT-AUTOFILL/extension

# Create necessary files
touch contentScript.js popup.css popup.html popup.js 

# Download jQuery library
curl -o jquery-3.7.1.min.js https://code.jquery.com/jquery-3.7.1.min.js

echo "Repository structure created successfully!"
```

Save this script as [`setup.sh`](http://setup.sh), and run it in your terminal to quickly generate the repository.

# Manifesting `manifest.json`

The `manifest.json` file is the backbone of the Chrome extension. It defines the extension's metadata, permissions, and how it interacts with the browser. Here’s a breakdown of the provided `manifest.json`:

```json
{
  "manifest_version": 3,
  "name": "CMT Author Auto-Filler",
  "version": "1.0",
  "description": "Auto-fills author details in Microsoft CMT.",
  "permissions": ["storage", "scripting", "activeTab", "declarativeContent"],
  "host_permissions": [
    "https://cmt3.research.microsoft.com/*/Track/*/Submission/Create"
  ],
  "action": {
    "default_popup": "extension/popup.html"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["extension/contentScript.js"]
    }
  ]
}
```

#### Key Fields:

1. `manifest_version`:
    
    * Specifies the version of the Chrome extension API. We use version 3, which is the latest and more secure version.
        
2. `name` and `version`:
    
    * Define the extension's name and version for identification and updates.
        
3. `description`:
    
    * A short description of the extension’s purpose, displayed in the Chrome Web Store.
        
4. `permissions`:
    
    * Grants necessary permissions:
        
        * `storage`: For saving author data.
            
        * `scripting`: To execute scripts on the target web pages.
            
        * `activeTab`: Allows actions on the active tab.
            
        * `declarativeContent`: Specifies when the extension is active.
            
5. `host_permissions`:
    
    * Limits the extension to operate only on specific URLs. In this case, it targets the submission creation page of the Microsoft CMT.
        
6. `action`:
    
    * Points to the popup interface (`popup.html`) that appears when the extension icon is clicked.
        
7. `content_scripts`:
    
    * Specifies scripts (`contentScript.js`) to be injected into web pages matching the given patterns. Here, it applies to all URLs (`<all_urls>`).
        

# HTML and CSS Code for Popup

Below is the **popup HTML** and **CSS** for the extension. These files define the structure and styling of the extension's interface.

#### `popup.html`

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CMT Author Auto-Fill</title>
  <link rel="stylesheet" href="./popup.css">
  <script src="jquery-3.7.1.min.js"></script>
</head>

<body>
  <h1>CMT Author Auto-Fill</h1>

  <button type="button" id="autoFillAuthors">Fill</button>
  <div id="profileButtons">
    <button class="profile-button" data-profile="profile1">Profile 1</button>
    <button class="profile-button" data-profile="profile2">Profile 2</button>
    <button class="profile-button" data-profile="profile3">Profile 3</button>
    <button class="profile-button" data-profile="profile4">Profile 4</button>
  </div>

  <form id="authorForm">
    <div id="authorFields">
      <!-- Author 1 -->
      <div class="author" data-author-index="1">
        <h2>Author 1</h2>
        <label>Email:</label>
        <input type="email" id="email1" placeholder="Email">
        <label>First Name:</label>
        <input type="text" id="name1" placeholder="First Name">
        <label>Last Name:</label>
        <input type="text" id="surname1" placeholder="Last Name">
        <label>Organization:</label>
        <input type="text" id="organization1" placeholder="Organization">
        <label>Country:</label>
        <select id="country1">
          <option value="">Select...</option>
          <option value="IN">India</option>
          <option value="HU">Hungary</option>
          <option value="US">United States</option>
          <option value="UK">United Kingdom</option>
          <option value="CA">Canada</option>
        </select>
      </div>

      <!-- Additional Authors (2-4) -->
      <!-- ... Same structure repeated for Author 2, Author 3, and Author 4 ... -->

    </div>
    <button type="button" id="saveAuthors">Save Authors</button>
  </form>
  <script src="popup.js"></script>
</body>

</html>
```

#### `popup.css`

```css
body {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 20px;
  width: 450px;
  background-color: #f3f3f3;
  box-sizing: border-box;
  color: #333;
}

h1 {
  font-size: 18px;
  text-align: center;
  color: #005a9e;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

h2 {
  font-size: 16px;
  margin-top: 20px;
  color: #333;
  padding-left: 5px;
  border-left: 3px solid #0078d7;
}

label {
  font-size: 14px;
  font-weight: bold;
  margin-top: 10px;
  display: block;
  color: #333;
}

input,
select {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 3px;
  box-sizing: border-box;
  font-size: 14px;
  background-color: #fff;
  color: #333;
}

button {
  margin-top: 15px;
  padding: 10px 15px;
  border: none;
  border-radius: 3px;
  background-color: #0078d7;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

button:hover {
  background-color: #005a9e;
}

.author {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

#profileButtons {
  text-align: center;
  margin-bottom: 15px;
}

.profile-button {
  margin: 5px;
  padding: 8px 12px;
  border: 1px solid #0078d7;
  border-radius: 3px;
  background-color: #e6f4ff;
  color: #005a9e;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.profile-button:hover {
  background-color: #0078d7;
  color: #fff;
}

#saveAuthors {
  width: 100%;
}

#autoFillAuthors {
  width: 100%;
  margin-top: 10px;
}
```

# Understanding the Engine of CMT Author Auto-Fill

The `popup.js` file is the brain of the Chrome extension, responsible for saving, loading, and auto-filling author details. Let’s go step by step and understand its functionality, introducing each feature as it appears in the code.

## Saving Author Profiles: Let’s Start with Storing Author Details

The first feature users need is the ability to save their author information for later use. This is critical for quickly reusing profiles across different submissions.

```javascript
$(document).ready(function() {
  let activeProfile = 'profile1'; 
  
  $('#saveAuthors').on('click', function() {
    const authors = [];
    for (let i = 1; i <= 4; i++) {
      authors.push({
        email: $(`#email${i}`).val(),
        name: $(`#name${i}`).val(),
        surname: $(`#surname${i}`).val(),
        organization: $(`#organization${i}`).val(),
        country: $(`#country${i}`).val(),
      });
    }
    chrome.storage.sync.set({ [activeProfile]: authors }, function() {
      alert(`Authors saved for ${activeProfile}!`);
    });
  });
```

**How It Works**:

1. **Active Profile**: A default profile (`profile1`) is set when the script loads.
    
2. **Event Listener**: When the user clicks the "Save Authors" button, the script:
    
    * Collects the input values from all fields for all four authors.
        
    * Creates an array of objects (`authors`) to hold these details.
        
3. **Save to Chrome Storage**: The collected data is saved to Chrome's sync storage under the `activeProfile` key.
    
4. **Feedback**: A success message is displayed to confirm the save.
    

## Loading Profiles: Fetching Saved Information

Now that users can save their profiles, they’ll need a way to retrieve them when required. This feature ensures that data saved in one session can be reused later.

```javascript
  function loadProfile(profile) {
    chrome.storage.sync.get([profile], function(result) {
      if (result[profile] && result[profile].length > 0) {
        result[profile].forEach(function(author, index) {
          const i = index + 1;
          $(`#email${i}`).val(author.email || '');
          $(`#name${i}`).val(author.name || '');
          $(`#surname${i}`).val(author.surname || '');
          $(`#organization${i}`).val(author.organization || '');
          $(`#country${i}`).val(author.country || '');
        });
        console.log(`Loaded ${profile}`);
      } else {
        console.log(`No saved authors found for ${profile}`);
        clearFields();
      }
    });
  }
```

**How It Works**:

1. **Fetch Data**: The function retrieves saved data from Chrome storage for the selected profile.
    
2. **Populate Fields**: If data exists, it fills the input fields with the corresponding values for each author.
    
3. **Handle Missing Data**: If no data is found, it resets all input fields by calling the `clearFields()` function.
    
4. **Debugging**: Logs are added for clarity when profiles are loaded or missing.
    

## Switching Profiles: Managing Multiple Profiles

Sometimes, users may need to save and load different sets of author details. This is where the profile buttons come into play.

```javascript
  $('.profile-button').on('click', function() {
    activeProfile = $(this).data('profile');
    loadProfile(activeProfile);
  });
```

**How It Works**:

1. **Profile Buttons**: Each button corresponds to a profile (e.g., Profile 1, Profile 2).
    
2. **Active Profile Update**: Clicking a button sets the `activeProfile` to the selected profile.
    
3. **Load Data**: The script calls `loadProfile()` to populate the fields with data from the selected profile.
    

This feature ensures that users can easily switch between saved profiles.

## Clearing Input Fields: Resetting Form Data

Let’s introduce a utility function that ensures all fields are reset when needed, such as when switching to a profile without saved data.

```javascript
  function clearFields() {
    for (let i = 1; i <= 4; i++) {
      $(`#email${i}`).val('');
      $(`#name${i}`).val('');
      $(`#surname${i}`).val('');
      $(`#organization${i}`).val('');
      $(`#country${i}`).val('');
    }
  }
```

**How It Works**:

* Loops through all input fields for the four authors and sets their values to empty.
    
* Keeps the form clean and ensures no residual data is displayed.
    

## Auto-Fill on the Active Tab: The Magic Button

Finally, the most exciting feature is the "Fill" button. This feature enables users to automatically fill the CMT form in the browser.

```javascript
  $('#autoFillAuthors').on('click', function() {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, { action: 'autoFillAuthors', profile: activeProfile });
    });
  });
```

**How It Works**:

1. **Active Tab Identification**: The script identifies the current active browser tab.
    
2. **Message Sending**: It sends a message to the `contentScript.js` running on the active tab, instructing it to auto-fill the form using data from the `activeProfile`.
    

This ensures seamless integration between the popup and the web page.

### Initial Profile Load: Setting Up the Default Profile

When the popup first opens, it should display the data for the default profile (`profile1`).

```javascript
  loadProfile(activeProfile);
});
```

**How It Works**:

* Automatically calls `loadProfile()` for the default profile when the popup is loaded.
    

## Full Code for `popup.js`

Here’s the entire code for `popup.js`:

```javascript
$(document).ready(function() {
  let activeProfile = 'profile1'; 
  
  $('#saveAuthors').on('click', function() {
    const authors = [];
    for (let i = 1; i <= 4; i++) {
      authors.push({
        email: $(`#email${i}`).val(),
        name: $(`#name${i}`).val(),
        surname: $(`#surname${i}`).val(),
        organization: $(`#organization${i}`).val(),
        country: $(`#country${i}`).val(),
      });
    }
    chrome.storage.sync.set({ [activeProfile]: authors }, function() {
      alert(`Authors saved for ${activeProfile}!`);
    });
  });

 
  function loadProfile(profile) {
    chrome.storage.sync.get([profile], function(result) {
      if (result[profile] && result[profile].length > 0) {
        result[profile].forEach(function(author, index) {
          const i = index + 1;
          $(`#email${i}`).val(author.email || '');
          $(`#name${i}`).val(author.name || '');
          $(`#surname${i}`).val(author.surname || '');
          $(`#organization${i}`).val(author.organization || '');
          $(`#country${i}`).val(author.country || '');
        });
        console.log(`Loaded ${profile}`);
      } else {
        console.log(`No saved authors found for ${profile}`);
        clearFields();
      }
    });
  }

  function clearFields() {
    for (let i = 1; i <= 4; i++) {
      $(`#email${i}`).val('');
      $(`#name${i}`).val('');
      $(`#surname${i}`).val('');
      $(`#organization${i}`).val('');
      $(`#country${i}`).val('');
    }
  }

  $('.profile-button').on('click', function() {
    activeProfile = $(this).data('profile');
    loadProfile(activeProfile);
  });

  $('#autoFillAuthors').on('click', function() {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, { action: 'autoFillAuthors', profile: activeProfile });
    });
  });

  
  loadProfile(activeProfile);
});
```

# Understanding the Heart of Automation

The `contentScript.js` is the most critical file in the Chrome extension. It directly interacts with the webpage, automating the process of filling the CMT form with author details. Let’s take a journey through this file in a logical flow, addressing specific user needs at every step.

## Handling Communication Between Popup and Content Script

When users click the "Fill" button in the popup, the extension needs to communicate this action to the content script. This is the first piece of functionality that ensures seamless communication.

```javascript
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'autoFillAuthors') {
      const profileKey = request.profile || 'profile1'; // Default to profile1 if not specified
      chrome.storage.sync.get([profileKey], (result) => {
          const authors = result[profileKey] || [];
          if (authors.length === 0) {
              alert(`No authors to fill for ${profileKey}. Please save author details first.`);
              return;
          }
          fillAuthorsSequentially(authors);
      });
  }
});
```

##### How It Works:

1. **Listening for Messages**:
    
    * The `chrome.runtime.onMessage.addListener` listens for actions triggered by the popup.
        
2. **Action Check**:
    
    * Checks if the message action is `autoFillAuthors`. If it is, the script proceeds to handle the request.
        
3. **Fetching Profile Data**:
    
    * Retrieves saved author details from Chrome storage for the specified profile (defaults to `profile1` if none is provided).
        
4. **Handling Missing Data**:
    
    * If no data exists for the profile, it alerts the user to save details first and exits.
        
5. **Calling the Filler Function**:
    
    * Passes the retrieved author data to the `fillAuthorsSequentially()` function to handle the auto-fill process.
        

This ensures the content script knows when to act and what data to use.

## Interacting with Knockout.js Forms

The CMT system uses Knockout.js for its forms, which requires special handling to ensure the inputs are updated correctly. This is where the `setKnockoutValue` function comes in.

```javascript
function setKnockoutValue(inputElement, value) {
  return new Promise((resolve) => {
      if (inputElement) {
          inputElement.focus();
          inputElement.value = value;
          inputElement.dispatchEvent(new Event('input', { bubbles: true }));
          inputElement.dispatchEvent(new Event('change', { bubbles: true }));
          console.log(`Set value for: ${inputElement.placeholder || inputElement.name}`);
      }
      setTimeout(resolve, 1);
  });
}
```

##### How It Works:

1. **Focus and Value Assignment**:
    
    * The function focuses on the input element and sets its value programmatically.
        
2. **Triggering Events**:
    
    * Dispatches `input` and `change` events to ensure Knockout.js detects the value change and updates its internal bindings.
        
3. **Promise for Sequential Execution**:
    
    * Returns a `Promise`, allowing this function to be used in an asynchronous flow (important for sequentially filling fields).
        
4. **Debugging Logs**:
    
    * Logs which field is being updated for easier debugging.
        

This function is the backbone for updating fields dynamically in a Knockout.js-driven form.

## Sequentially Filling Author Details

Now that the system can receive messages and update fields, the next step is to handle multiple authors. Users need a way to fill out the details for all authors in sequence.

```javascript
function fillAuthorsSequentially(authors) {
  let index = 0;

  function processNextAuthor() {
      if (index >= authors.length) {
          console.log('All authors have been added successfully.');
          alert('All authors have been added!');
          return;
      }

      const author = authors[index];
      const addButton = document.querySelector('button[data-bind*="showDialog(true)"]');
```

##### How It Works (Part 1):

1. **Sequential Execution**:
    
    * A recursive function, `processNextAuthor`, is used to handle one author at a time.
        
2. **Stopping Condition**:
    
    * If all authors have been processed, it logs success and alerts the user.
        
3. **Finding the "Add Author" Button**:
    
    * Locates the button to open the "Add Author" form and clicks it to proceed.
        

## Filling the Author Form

Once the "Add Author" button is clicked, the script needs to fill the form with the author’s details.

```javascript
          setTimeout(async () => {
              const form = document.querySelector('form[data-bind*="submit: function () { $parent.addAuthor($data); }"]');

              if (!form) {
                  alert('Author form not found.');
                  return;
              }

              const emailField = form.querySelector('input[data-bind*="value: email"]');
              const firstNameField = form.querySelector('input[data-bind*="value: firstName"]');
              const lastNameField = form.querySelector('input[data-bind*="value: lastName"]');
              const organizationField = form.querySelector('input[data-bind*="value: organization"]');
              const countryDropdown = form.querySelector('select[data-bind*="value: countryCode"]');
              const submitButton = form.querySelector('button[type="submit"]');
```

##### How It Works (Part 2):

1. **Finding the Form**:
    
    * Identifies the author form using unique attributes tied to Knockout.js bindings.
        
2. **Locating Fields**:
    
    * Finds all the input fields (email, first name, last name, organization, and country dropdown) required to fill the author details.
        
3. **Error Handling**:
    
    * Alerts the user if the form or any required field is not found.
        

## Submitting the Form and Moving to the Next Author

Finally, after filling in all fields, the form needs to be submitted before proceeding to the next author.

```javascript
              if (emailField) await setKnockoutValue(emailField, author.email || '');
              if (firstNameField) await setKnockoutValue(firstNameField, author.name || '');
              if (lastNameField) await setKnockoutValue(lastNameField, author.surname || '');
              if (organizationField) await setKnockoutValue(organizationField, author.organization || '');

              if (countryDropdown) {
                  countryDropdown.value = author.country || '';
                  countryDropdown.dispatchEvent(new Event('change', { bubbles: true }));
                  console.log(`Selected country: ${author.country}`);
                  await new Promise((resolve) => setTimeout(resolve, 1));
              }

              console.log(`Filled Author ${index + 1}:`, author);

              if (submitButton) {
                  submitButton.click();
                  console.log(`Clicked Submit button for Author ${index + 1}`);

                  index++;
                  setTimeout(processNextAuthor, 2);
              } else {
                  alert('Submit button not found in the form!');
              }
          }, 1);
      } else {
          alert('Add button not found on the page.');
      }
  }

  processNextAuthor();
}
```

##### How It Works (Part 3):

1. **Setting Field Values**:
    
    * Uses the `setKnockoutValue` function to set the values for all fields.
        
    * Handles the country dropdown separately to ensure proper event dispatch.
        
2. **Submitting the Form**:
    
    * Clicks the submit button to add the current author.
        
3. **Recursive Call**:
    
    * After a short delay, moves to the next author by incrementing the `index` and calling `processNextAuthor`.
        
4. **Error Handling**:
    
    * Alerts the user if the submit button or the "Add Author" button is not found.
        

### Full Code for `contentScript.js`

Here’s the full, polished version of the `contentScript.js` file:

```javascript
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'autoFillAuthors') {
      const profileKey = request.profile || 'profile1'; // Default to profile1 if not specified
      chrome.storage.sync.get([profileKey], (result) => {
          const authors = result[profileKey] || [];
          if (authors.length === 0) {
              alert(`No authors to fill for ${profileKey}. Please save author details first.`);
              return;
          }
          fillAuthorsSequentially(authors);
      });
  }
});

function setKnockoutValue(inputElement, value) {
  return new Promise((resolve) => {
      if (inputElement) {
          inputElement.focus();
          inputElement.value = value;
          inputElement.dispatchEvent(new Event('input', { bubbles: true }));
          inputElement.dispatchEvent(new Event('change', { bubbles: true }));
          console.log(`Set value for: ${inputElement.placeholder || inputElement.name}`);
      }
      setTimeout(resolve, 1);
  });
}

function fillAuthorsSequentially(authors) {
  let index = 0;

  function processNextAuthor() {
      if (index >= authors.length) {
          console.log('All authors have been added successfully.');
          alert('All authors have been added!');
          return;
      }

      const author = authors[index];
      const addButton = document.querySelector('button[data-bind*="showDialog(true)"]');

      if (addButton) {
          addButton.click();
          console.log(`Clicked Add button for Author ${index + 1}`);

          setTimeout(async () => {
              const form = document.querySelector('form[data-bind*="submit: function () { $parent.addAuthor($data); }"]');

              if (!form) {
                  alert('Author form not found.');
                  return;
              }

              const emailField = form.querySelector('input[data-bind*="value: email"]');
              const firstNameField = form.querySelector('input[data-bind*="value: firstName"]');
              const lastNameField = form.querySelector('input[data-bind*="value: lastName"]');
              const organizationField = form.querySelector('input[data-bind*="value: organization"]');
              const countryDropdown = form.querySelector('select[data-bind*="value: countryCode"]');
              const submitButton = form.querySelector('button[type="submit"]');

              if (emailField) await setKnockoutValue(emailField, author.email || '');
              if (firstNameField) await setKnockoutValue(firstNameField, author.name || '');
              if (lastNameField) await setKnockoutValue(lastNameField, author.surname || '');
              if (organizationField) await setKnockoutValue(organizationField, author.organization || '');

              if (countryDropdown) {
                  countryDropdown.value = author.country || '';
                  countryDropdown.dispatchEvent(new Event('change', { bubbles: true }));
                  console.log(`Selected country: ${author.country}`);
                  await new Promise((resolve) => setTimeout(resolve, 1));
              }

              console.log(`Filled Author ${index + 1}:`, author);

              if (submitButton) {
                  submitButton.click();
                  console.log(`Clicked Submit button for Author ${index + 1}`);

                  index++;
                  setTimeout(processNextAuthor, 2);
              } else {
                  alert('Submit button not found in the form!');
              }
          }, 1);
      } else {
          alert('Add button not found on the page.');
      }
  }

  processNextAuthor();
}
```

# Conclusion

Creating a Chrome extension like the **CMT Author Auto-Fill** empowers users to save time and eliminate repetitive tasks by automating the process of filling author details in Microsoft CMT. Throughout this guide, we walked you through the step-by-step creation of the extension, including:

* Setting up the **manifest.json** file for defining extension permissions and functionality.
    
* Developing the **popup.js** for saving and loading author profiles.
    
* Implementing **contentScript.js** to dynamically interact with the CMT webpage, handle form filling, and integrate Knockout.js-based inputs.
    

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1734731531151/d664b5ca-77cc-4094-95a6-3c0d18b85d2c.png align="center")

The extension's workflow is simple yet powerful:

1. Users save author details for up to four profiles using the popup interface.
    
2. By clicking the "Fill" button, the extension auto-fills the CMT author form based on the selected profile.
    

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1734731549494/4b86436d-8d23-4a95-b5d0-34376797c3a8.png align="center")

This powerful extension streamlines the form-filling process and boosts productivity, especially for researchers and authors submitting to multiple conferences.

For the **complete source code**, including all files and detailed explanations, check out this [GitHub repository](https://github.com/arya2004/cmt-autofill/).