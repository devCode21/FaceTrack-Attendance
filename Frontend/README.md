# ClassTrack Frontend – React Dashboard for Multi-Face Recognition Attendance System

This repository contains the **React frontend** for the ClassTrack system. The application provides an interface for users to upload classroom videos, send them to the backend for processing, and visualize the generated attendance results.

The frontend communicates with a backend face recognition pipeline that detects and identifies students from classroom recordings.

---

# Project Overview

The ClassTrack frontend is designed to provide a simple and responsive interface for managing automated attendance using video input.

The application allows users to:

* Log into the system
* Upload classroom videos
* Send videos to the backend processing server
* View generated attendance reports
* Navigate results through a dashboard interface

---

# Tech Stack

* **React.js** – Frontend framework
* **Redux Toolkit** – Global state management
* **React Router DOM** – Page routing
* **Tailwind CSS** – Styling and UI design
* **Axios / Fetch API** – Backend API communication
* **LocalStorage** – Session persistence

---

# Project Structure

---

# Application Workflow

1. User logs into the system.
2. User uploads a classroom video through the upload interface.
3. The frontend sends the video to the backend API.
4. Backend processes the video and generates attendance data.
5. The frontend receives the response and displays the results on the dashboard.

---

# State Management

The application uses **Redux Toolkit** to manage global state.

The store maintains:

* User authentication data
* Uploaded video status
* Processed attendance results

This allows multiple components to access shared data without passing props across multiple layers.

---

# Session Persistence

Redux state resets when the page refreshes. To maintain the login session:

* Authentication tokens are stored in **LocalStorage**
* On application load, stored tokens are used to restore the session
* Data is cleared when the user logs out

---

# Performance Optimization

React hooks were used to improve rendering performance:

* **useMemo** – Caches computed values
* **useCallback** – Prevents unnecessary function recreation

These optimizations help reduce unnecessary re-renders and improve UI responsiveness.

---

# Challenges Faced

### Cross-Origin Communication

During development, the frontend and backend were running on different servers, causing cross-origin request issues. This was resolved by enabling **CORS configuration** on the backend.

### State Sharing Across Components

Multiple pages required access to the same data (authentication, processing results). Redux Toolkit was implemented to manage centralized application state.

### Maintaining Login Sessions

Refreshing the page caused Redux state to reset. LocalStorage was used to persist authentication tokens and restore the session when the application loads.

---

# Installation

Clone the repository:

```
git clone https://github.com/KadakSingh19/Class-Track
```

Navigate to the project folder:

```
cd frontend
```

Install dependencies:

```
npm install
```

Run the development server:

```
npm run dev
```

---

# Future Improvements

* Implement Redux Persist for better state persistence
* Add real-time processing status updates
* Improve dashboard analytics and visualization
* Enhance UI responsiveness for large datasets
