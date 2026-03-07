

# ClassTrack

ClassTrack is a full-stack face recognition based attendance system designed to demonstrate how modern deep learning models can be integrated into a practical web application. The system automates classroom attendance by detecting and identifying students from images or videos using a deep learning pipeline on the backend, while providing an intuitive web interface for teachers on the frontend. The project focuses on building a complete end-to-end system rather than just a standalone ML model, covering model inference, API design, database integration, and user interaction.

The backend is built using FastAPI and Python and is responsible for handling face detection, alignment, feature extraction, and identity matching. It integrates a multi-stage face recognition pipeline and communicates with a MongoDB database to store student embeddings, course information, and attendance records. The backend is containerized using Docker and deployed on AWS EC2, making it portable and easy to run across different environments. Detailed documentation for the backend, including the ML pipeline and deployment setup, is available in the backend folder.

The frontend is developed using React.js and Tailwind CSS to provide a clean and responsive user interface for teachers. It allows users to create and manage courses, upload classroom images or videos, and view attendance results in a dashboard-style layout. State management is handled carefully to ensure smooth interaction between components and efficient updates when attendance data changes. The frontend communicates with the backend through REST APIs and is designed to remain lightweight and fast.

Overall, ClassTrack is built as a system-level prototype intended for academic, learning, and portfolio purposes. It showcases the practical application of machine learning in a full-stack environment and emphasizes clean architecture, modular design, and real-world constraints such as low-compute deployment and privacy considerations, while clearly separating the concerns of the backend and frontend components.

### 📁 Project Modules
👉 **Frontend Documentation:** https://github.com/KadakSingh19/Class-Track/blob/main/Frontend/README.md
👉 **Backend Documentation:** [(https://github.com/devCode21/FaceTrack-Attendance/blob/main/Backend/readme.md)]


