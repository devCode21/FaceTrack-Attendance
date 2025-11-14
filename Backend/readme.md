# FaceAttendance Backend

A simple and clean backend service for **automatic face attendance** from classroom videos or images. The backend processes media, recognizes students, and updates attendance for a selected course.

---

# 📌 Overview

The system takes **videos or images** from the frontend, detects faces, matches them with stored embeddings, and marks attendance. No videos are stored.

The pipeline is fast, practical, and works on low-compute devices.

---

# 📂 Folder Structure

```
backend/
 ├── app.py
 ├── src/
 │    ├── components/
 │    ├── utils/
 │    ├── pipeline/
 │    └── database/
 ├── test/
 └── requirements.txt
```

---

# 🧠 Face Recognition Pipeline

The backend follows this simple flow:

1. **YOLO11n** → Detect faces (chosen for good speed + accuracy)
2. **MTCNN** → Align faces properly
3. **FaceNet** → Convert face to a 128-dim embedding
4. **Cosine Similarity** → Match with stored embeddings
5. Threshold = **0.80** to confirm identity

### Frame Skipping

To keep things fast, only **every 30th frame** of the video is processed.

### Experiments

* **EDSR** → Higher accuracy but way too slow → Removed
* **RetinaNet** → Same accuracy as YOLO but slower → Removed
* **YOLO11n** → Final choice

---

# 🗄️ Database (MongoDB)

Two collections are used:

### **Course Collection**

```
{
  _id: ObjectId,
  name: "teacher_name",
  course_name: "CourseTitle",
  password: "hashed_password",
  class_object_id: ObjectId
}
```

### **Class Collection**

```
{
  _id: ObjectId,
  className: "ECE_3A",
  class_id: "ID123",
  embeddings: [
    {
      student_name: "Ravi",
      embedding: [...],
      student_id: "S101"
    }
  ]
}
```

---

# 🔗 API Endpoints

### **POST /attendance_image/{course_id}**

Process a single image and update attendance.

### **POST /attendance_data/{course_id}**

Process a classroom video and update attendance.

### **POST /login_existing_course**

Teacher login.

### **POST /Create_New_Course**

Create a new course.

---

# 🔧 Running Locally

```
uvicorn app:app --reload
```

---

# 🐳 Docker Setup

(Coming Soon)

---

# ☁️ AWS Deployment

(Coming Soon)

---

# 🔮 Future Improvements

* Try ArcFace for better accuracy
* Add ONNX for faster inference
* Add simple dashboard for attendance
* Add GPU support

---

# 🤝 Contributing

Open to suggestions and improvements.

# 📄 License

Add your preferred license (MIT, etc.).
