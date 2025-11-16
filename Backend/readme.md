# FaceAttendance Backend


# 📌 Overview

This backend receives classroom **videos or images**, processes them using a deep learning pipeline, identifies students through face embeddings, and updates attendance for a selected course.

**Key Highlights:**

* No videos stored → privacy & low cost
* Works on low-compute machines
* Frame skipping, model selection, and similarity scoring carefully optimized
* Clean FastAPI backend + MongoDB

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

# 🧠 Face Recognition Pipeline (Full Context)

The backend uses a **3-stage deep learning pipeline** followed by embedding matching.

## **1️⃣ YOLO11n — Face Detection**

We tested multiple detectors and finalized **YOLO11n** because:

* Excellent **speed–accuracy trade-off**
* Works well on **CPU-level hardware**
* Faster than RetinaNet with similar accuracy
* Other YOLO variants gave slightly better accuracy but were slower

👉 **Final decision:** YOLO11n is the best for real-time attendance.

## **2️⃣ MTCNN — Face Alignment**

Faces in classroom videos are often tilted or partially rotated.

* MTCNN aligns faces properly
* Ensures consistent FaceNet embeddings
* light wieght model for alignment 

## **3️⃣ FaceNet — Embedding Generation**

We create a **512-dimension embedding** for each face.

* Stable identity representation
* Works reliably even with low-resolution classroom frames

## **4️⃣ Cosine Similarity — Identity Matching**

We tested different similarity measures:

* Euclidean (L2)
* Manhattan
* Dot Product
* Cosine Similarity

Cosine gave **the best separation between different students** during testing on our small dataset.

👉 **Threshold used:** `0.80`

A match is valid if:

```
cosine_similarity >= 0.80
```

During testing, we experimented with different cosine similarity thresholds. When the threshold was set below 0.80, the number of false positives increased significantly, meaning the system started marking the wrong students as present. Even though lower thresholds improved true positive detection, the false positives were too high to use in a real classroom environment.

To keep the system reliable and avoid incorrect attendance marks, we decided to prioritize reducing false positives, even if it meant compromising a bit on true positive rates.
Therefore, the threshold 0.80 was

## **5️⃣ Frame Skipping — Every 30th Frame**

Due to limited hardware (no GPU):

* Processing every frame was too slow
* Skipping too many frames missed faces

We found **30th frame** to be the ideal balance (still experminting on it ):

* Fast enough to process full classroom videos
* Still captures each student multiple times

---

# 🧪 Model Experiments — Full Reasoning

This section includes everything we tested and why we kept or removed each model.

## **🔹 EDSR (Super Resolution)**

Goal: Improve face quality → improve embeddings.

**Result:**

* Slight improvement in accuracy
* BUT extremely slow
* Too heavy for real-time inference
* CPU-only machine couldn’t handle it

👉 **Rejected** due to speed.

---

## **🔹 RetinaNet (Face Detection)**

Goal: Replace YOLO, see if accuracy improves.

**Result:**

* Accuracy similar to YOLO11n
* Slower detection
* No real accuracy benefit

👉 **Rejected** because YOLO11n gives same output but much faster.

---

## **🔹 YOLO11n (Final Choice)**

* Good accuracy
* Very fast
* Works well without GPU

👉 **Selected as final detection model.**

---

# 🔬 Qualitative Benchmarks (Based on Observations)

Since we didn’t have strong hardware (GPU), we used **practical, observed benchmarks**:

### **Detection Speed**

* **YOLO11n** → Fastest detectable performance on our setup
* **RetinaNet** → Noticeably slower

### **Embedding Quality**

* **FaceNet** performed consistently well
* EDSR improved quality but slowed system drastically

### **Matching Accuracy**

* Cosine similarity gave the most stable results
* Threshold 0.80 minimized false positives

### **End-to-end Pipeline Speed**

* Processing every frame → too slow
* Every 10th frame → too many mismatches
* **Every 30th frame → perfect balance**

These decisions are practical, based on multiple test videos and real constraints.

---

# 🗄️ Database (MongoDB)

The backend uses two collections.

## **Course Collection**

Stores teacher’s course.

```
{
  _id: ObjectId,
  name: "teacher_name",
  course_name: "CourseTitle",
  password: "hashed_password",
  class_object_id: ObjectId
}
```

## **Class Collection**

Stores class metadata + student embeddings.

```
{
  _id: ObjectId,
  className: "ECE_3A",
  class_id: "ID123",
  embeddings: [
    {
      student_name: "Ravi",
      embedding: [...128-dim vector...],
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

Coming soon (not implemented yet).

---

# ☁️ AWS Deployment

Coming soon (planned for EC2 + Docker).

---

# 🔮 Future Improvements

* Use ArcFace for better embeddings
* Convert models to ONNX for speed
* Add GPU support when available
* Real-time face tracking
* Live dashboard for attendance

---

# 🤝 Contributing

Suggestions welcome.

# 📄 License

MIT / your choice.
