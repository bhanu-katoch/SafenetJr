# SafenetJr 👨‍👩‍👧‍👦🔒

SafenetJr is a real-time web application designed to help parents monitor and manage their children's internet activity. With a focus on **cybersecurity** and **child safety**, the app provides automated tracking and filtering of inappropriate websites using a custom-built Chrome extension and Machine Learning analytics.

## 🚀 Features

- Real-time monitoring of child's web browsing activity.
- Chrome extension that captures browsing history every 20 seconds.
- Automatic classification and reporting of inappropriate content using ML.
- Parent-child connection established securely via unique IDs.
- Periodic POST requests to send activity data to the server.
- Generates meaningful reports for parents to review.

## 🛠️ How It Works

### 1. Chrome Extension
- Preconfigured with **Parent ID** and **Child Number**.
- Fetches **Child ID** from the backend via a GET request.
- Establishes a secure connection.
- Sends the child’s browsing history every 20 seconds via POST request to the backend server.

### 2. Backend Server (Parent Side)
- Receives browsing history data.
- Uses **Machine Learning** algorithms to analyze and classify web content.
- Generates a report based on website categories and flagging inappropriate content.
- Provides a dashboard/interface for parental review.

## 🧠 Tech Stack

- **Frontend:** HTML, CSS, Javascript, Bootstrap
- **Backend:** Python, Django (adjust based on your implementation)
- **Extension:** Chrome Extensions API (JavaScript)
- **ML Model:** Custom-trained classifier for content filtering
- **Database:** Sqlite 
- **Other:** RESTful APIs, Cybersecurity best practices

## 📦 Installation

### Chrome Extension
1. Navigate to `chrome://extensions/`
2. Enable "Developer Mode"
3. Click **Load unpacked** and select the extension folder

### Backend Server
1. Clone this repo:
   ```bash
   git clone https://github.com/yourusername/safenetjr.git
   cd safenetjr
## 📽️ Demo Video

- [ Video1 ](https://drive.google.com/file/d/17WYVfqWe05A15dl-diLxGlNPbhrPbKA6/view?usp=drivesdk)
- [ Video2 ](https://drive.google.com/file/d/1yJZ21O3AalCOhr8asOfgD2hiao7jnbxq/view?usp=drivesdk)


