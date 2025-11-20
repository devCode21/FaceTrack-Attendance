
import React, { useState, useRef, useCallback } from "react";
import { motion } from "framer-motion";
import * as Icons from "lucide-react";

// ---------------- Toast Mock ----------------
const useToast = () => ({ push: (msg) => console.log("TOAST:", msg) });

const fade = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

// ---------------- Layout ----------------
const PageHeader = () => (
  <div className="w-full border-b border-zinc-800 bg-neutral-950/70 backdrop-blur-lg p-6 sticky top-0 z-40 shadow-xl">
    <div className="max-w-5xl mx-auto flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-600 to-indigo-600 flex items-center justify-center text-white font-bold">
          FR
        </div>
        <div>
          <h1 className="text-xl font-semibold text-neutral-100">Attendance Processing</h1>
          <p className="text-xs text-neutral-400">Powered by YOLO • MTCNN • ResNet</p>
        </div>
      </div>
      <button className="text-neutral-400 hover:text-red-400 transition flex items-center gap-2">
        <Icons.LogOut className="w-4 h-4" /> Logout
      </button>
    </div>
  </div>
);

// ---------------- Card Wrapper ----------------
const Card = ({ title, icon: Icon, children }) => (
  <motion.div
    variants={fade}
    initial="hidden"
    animate="show"
    className="bg-neutral-900/60 border border-zinc-800 backdrop-blur-xl rounded-2xl p-6 shadow-xl"
  >
    <div className="flex items-center gap-3 mb-4">
      <div className="p-2 rounded-md bg-neutral-800/50 border border-zinc-700">
        {Icon && <Icon className="w-5 h-5 text-sky-400" />}
      </div>
      <h3 className="text-lg font-semibold text-neutral-100">{title}</h3>
    </div>
    {children}
  </motion.div>
);

// ---------------- Step 1: Image Upload ----------------
const ImageUpload = ({ onUpload }) => {
  const [images, setImages] = useState([]);
  const ref = useRef(null);
  const toast = useToast();

  const addFiles = (files) => {
    const imgs = Array.from(files).filter((f) => f.type.startsWith("image/"));
    if (!imgs.length) return toast.push({ title: "No valid images" });
    setImages((prev) => [...prev, ...imgs].slice(0, 30));
  };

  return (
    <Card title="Upload Images" icon={Icons.Image}>
      <div
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => { e.preventDefault(); addFiles(e.dataTransfer.files); }}
        onClick={() => ref.current && ref.current.click()}
        className="border-2 border-dashed border-sky-500/40 rounded-xl p-8 text-center cursor-pointer hover:bg-neutral-800/30 transition"
      >
        <Icons.UploadCloud className="w-8 h-8 mx-auto text-sky-400" />
        <p className="text-neutral-400 mt-2 text-sm">Drag & drop or click to upload (Max 30)</p>
      </div>

      <input ref={ref} type="file" accept="image/*" multiple className="hidden" onChange={(e) => addFiles(e.target.files)} />

      {images.length > 0 && (
        <div className="mt-4">
          <div className="flex flex-wrap gap-3 max-h-40 overflow-auto p-2 bg-neutral-900/40 rounded-lg border border-zinc-700">
            {images.map((f, i) => (
              <div key={i} className="relative w-20 h-20 rounded-md overflow-hidden border border-zinc-700">
                <img src={URL.createObjectURL(f)} alt={`preview-${i}`} className="w-full h-full object-cover" />
                <button
                  onClick={() => setImages((s) => s.filter((_, idx) => idx !== i))}
                  className="absolute top-1 right-1 bg-red-600 text-white rounded-full p-1"
                >
                  <Icons.X className="w-3 h-3" />
                </button>
              </div>
            ))}
          </div>

          <button
            onClick={() => { onUpload(images); setImages([]); }}
            className="mt-4 w-full px-4 py-2 rounded-lg bg-sky-600 text-white font-medium hover:bg-sky-700"
            type="button"
          >
            Upload {images.length} Image(s)
          </button>
        </div>
      )}
    </Card>
  );
};

// ---------------- Step 2: Video Upload ----------------
const VideoUpload = ({ onUpload }) => {
  const [video, setVideo] = useState(null);
  const toast = useToast();

  return (
    <Card title="Upload Video" icon={Icons.Video}>
      <input
        type="file"
        accept="video/*"
        onChange={(e) => setVideo(e.target.files[0])}
        className="block w-full text-sm text-neutral-300 file:px-4 file:py-2 file:rounded-lg file:bg-sky-600/20 file:text-sky-300"
      />

      {video && (
        <div className="mt-3 p-3 bg-neutral-900/40 rounded-lg border border-zinc-700 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Icons.FileText className="w-5 h-5 text-sky-400" />
            <p className="text-sm text-neutral-200 truncate max-w-40">{video.name}</p>
          </div>
          <button onClick={() => setVideo(null)} className="text-red-500">Remove</button>
        </div>
      )}

      <button
        onClick={() => { if (video) { onUpload(video); setVideo(null); } }}
        className="mt-4 w-full px-4 py-2 rounded-lg bg-sky-600 text-white hover:bg-sky-700"
        type="button"
      >
        Upload Video
      </button>
    </Card>
  );
};

// ---------------- Step 3: Actions + Step 4: Reports ----------------
const AttendanceActions = ({ onDownload, onView }) => (
  <Card title="Attendance Actions" icon={Icons.CheckCircle}>
    <button className="w-full px-4 py-3 rounded-lg bg-indigo-600 text-white font-semibold hover:bg-indigo-700" type="button">
      Run Recognition
    </button>

    <div className="grid grid-cols-2 gap-3 mt-4">
      <button onClick={onDownload} className="px-4 py-2 rounded-lg border border-sky-500 text-sky-400 hover:bg-neutral-800/40" type="button">
        <Icons.Download className="w-4 h-4 inline mr-2" /> Download CSV
      </button>
      <button onClick={onView} className="px-4 py-2 rounded-lg border border-zinc-700 text-neutral-300 hover:bg-neutral-800/40" type="button">
        <Icons.Table className="w-4 h-4 inline mr-2" /> View Attendance
      </button>
    </div>
  </Card>
);

// ---------------- Instructions ----------------
const Instructions = () => (
  <Card title="Instructions" icon={Icons.Info}>
    <ul className="text-sm text-neutral-300 space-y-2">
      <li>1. Upload lecture images OR upload a full video.</li>
      <li>2. Click <strong>Run Recognition</strong> to process attendance.</li>
      <li>3. Use <strong>Download CSV</strong> to save results or <strong>View Attendance</strong> to inspect.</li>
    </ul>
  </Card>
);

// ---------------- Main Page ----------------
export default function TeacherAttendancePage() {
  const toast = useToast();

  // Use stable handlers instead of inline arrow functions in JSX
  const handleImageUpload = useCallback((files) => {
    // files is an array of File objects
    console.log("Images uploaded:", files.map((f) => f.name));
    toast.push({ title: "Images Uploaded", description: `${files.length} image(s)` });
  }, []);

  const handleVideoUpload = useCallback((video) => {
    console.log("Video uploaded:", video?.name);
    toast.push({ title: "Video Uploaded", description: video?.name });
  }, []);

  const handleDownloadCSV = useCallback(() => {
    // mock CSV
    const csv = "id,name,status,time\n1,Student A,Present,09:05 AM";
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `attendance-${new Date().toISOString()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }, []);

  const handleViewAttendance = useCallback(() => {
    // In production this would navigate / open modal. For design focus, we'll just log.
    console.log("View Attendance clicked");
  }, []);

  return (
    <div className="min-h-screen bg-black text-neutral-200">
      <PageHeader />

      <div className="max-w-5xl mx-auto px-6 py-10 space-y-10">
        <motion.h2
          variants={fade}
          initial="hidden"
          animate="show"
          className="text-3xl font-bold text-neutral-100 mb-4"
        >
          Process Lecture Attendance
        </motion.h2>

        {/* STEPS IN ORDER */}
        <div className="space-y-10">
          <ImageUpload onUpload={handleImageUpload} />
          <VideoUpload onUpload={handleVideoUpload} />
          <AttendanceActions onDownload={handleDownloadCSV} onView={handleViewAttendance} />
          <Instructions />
        </div>
      </div>

      <footer className="border-t border-zinc-800 bg-neutral-900/60 mt-8">
        <div className="max-w-5xl mx-auto px-6 py-6 flex items-center justify-between text-sm text-neutral-500">
          <div>© {new Date().getFullYear()} FaceRec Attendance</div>
          <div>YOLO • MTCNN • ResNet • MongoDB</div>
        </div>
      </footer>
    </div>
  );
}
