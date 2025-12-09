import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import * as Icons from "lucide-react";
import axios from "axios";
import { useSelector } from "react-redux";
import { get_attendance_from_video, get_attendance_from_image } from "../components/BackendApi";

export default function CreativeAttendancePage() {
  const { CourseID, formdata , students } = useSelector((state) => state.Data);
  console.log(students)
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const fileRef = useRef(null);
  const bgRef = useRef(null);

  // -----------------------------------------
  // Parallax background movement
  // -----------------------------------------
  useEffect(() => {
    const handler = (e) => {
      const x = (e.clientX / window.innerWidth - 0.5) * 35;
      const y = (e.clientY / window.innerHeight - 0.5) * 35;
      if (bgRef.current) bgRef.current.style.transform = `translate(${x}px, ${y}px)`;
    };
    window.addEventListener("mousemove", handler);
    return () => window.removeEventListener("mousemove", handler);
  }, []);

  // -----------------------------------------
  // Score color badge
  // -----------------------------------------
  const confidenceColor = (score) => {
    if (score >= 0.75) return "text-green-400";
    if (score >= 0.45) return "text-yellow-400";
    return "text-red-400";
  };

  // -----------------------------------------
  // Process Attendance
  // -----------------------------------------
  const processAttendance = async () => {
    if (!file) return alert("Select a file first");
    if (loading) return;

    setLoading(true);
    setResults(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      let resp;

      if (file.type.startsWith("image")) {
        resp = await axios.post(get_attendance_from_image + CourseID, formData);
      } else {
        resp = await axios.post(get_attendance_from_video + CourseID, formData);
      }

      if (resp.status === 200) {
        alert("Attendance Processed");
        setResults(resp.data.results);
      }
    } catch (err) {
      alert("Failed to process");
    }

    setLoading(false);
  };

  return (
    <div className="relative min-h-screen bg-black text-white overflow-hidden">

      {/* Parallax Background */}
      <div ref={bgRef} className="fixed inset-0 -z-10 transition-transform duration-300">
        <div className="absolute top-20 left-10 w-72 h-72 bg-sky-600/30 blur-3xl rounded-full"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-600/30 blur-3xl rounded-full"></div>
      </div>

      {/* HEADER */}
      <header className="w-full border-b border-white/10 p-6 bg-black/50 backdrop-blur-xl sticky top-0 z-20">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-sky-500 to-indigo-600 flex items-center justify-center text-xl font-bold">
            FR
          </div>
          <div>
            <h1 className="text-xl font-semibold">Attendance Processor</h1>
            <p className="text-xs text-neutral-400">Smart Recognition System</p>
          </div>
        </div>
      </header>

      {/* MAIN */}
      <main className="max-w-4xl mx-auto px-6 py-10 space-y-10">

        {/* CLASS DETAILS */}
        <motion.div
          initial={{ opacity: 0, x: 40 }}
          animate={{ opacity: 1, x: 0 }}
          className="p-8 rounded-3xl bg-neutral-900/60 border border-white/10 shadow-xl"
        >
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <Icons.BadgeInfo className="text-sky-400" /> Class Details
          </h2>

          <div className="mt-4 p-4 rounded-xl bg-black/30 border border-white/10 text-lg space-y-1">
            <p>
              <span className="font-semibold text-white">Class :</span> {formdata?.class_name}
            </p>
            <p>
              <span className="font-semibold text-white">Course :</span> {formdata?.course_name}
            </p>
          </div>
        </motion.div>

        {/* FILE UPLOAD */}
        <motion.div
          initial={{ opacity: 0, x: 40 }}
          animate={{ opacity: 1, x: 0 }}
          className="p-10 rounded-3xl bg-neutral-900/60 border border-white/10 shadow-xl text-center"
        >
          <h2 className="text-xl font-semibold mb-6 flex items-center justify-center gap-2">
            <Icons.UploadCloud className="text-sky-400" /> Upload File
          </h2>

          <div
            onClick={() => !loading && fileRef.current.click()}
            className={`cursor-pointer p-10 border-2 border-dashed border-sky-500/40 rounded-2xl transition ${
              loading ? "opacity-50 pointer-events-none" : "hover:bg-neutral-800/40"
            }`}
          >
            <Icons.FolderOpen className="w-12 h-12 mx-auto text-sky-400" />
            <p className="text-neutral-300 mt-2 text-sm">Click to choose image or video</p>
          </div>

          <input
            type="file"
            className="hidden"
            ref={fileRef}
            accept="image/*,video/*"
            disabled={loading}
            onChange={(e) => setFile(e.target.files[0])}
          />

          {file && <p className="mt-4 text-neutral-300">Selected: {file.name}</p>}

          <button
            disabled={loading}
            onClick={processAttendance}
            className="mt-6 w-full py-4 bg-indigo-600 hover:bg-indigo-700 rounded-xl font-semibold text-lg shadow-lg"
          >
            {loading ? (
              <div className="flex items-center justify-center gap-3">
                <Icons.Loader2 className="w-5 h-5 animate-spin" />
                Processing...
              </div>
            ) : (
              "Process File"
            )}
          </button>
        </motion.div>

        {/* RESULTS */}
        {results && (
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            className="p-8 rounded-3xl bg-neutral-900/60 border border-white/10 shadow-xl"
          >
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Icons.Users className="text-sky-400" /> Recognized Students
            </h2>

            <div className="grid gap-4">
              {results.map((item, idx) => {
                const name = Object.keys(item)[0];
                const score = Object.values(item)[0];

                return (
                  <div
                    key={idx}
                    className="flex justify-between bg-neutral-800/50 border border-neutral-700 p-3 rounded-xl"
                  >
                    <span className="font-medium text-white">{name}</span>
                    <span className={`${confidenceColor(score)} font-mono text-lg`}>
                      {(score * 100).toFixed(2)}%
                    </span>
                  </div>
                );
              })}
            </div>

            <button
              onClick={() => setShowModal(true)}
              className="w-full mt-6 py-4 rounded-xl border border-neutral-700 hover:bg-neutral-800/40 text-lg font-semibold flex items-center justify-center gap-2"
            >
              <Icons.Table className="w-5 h-5" />
              View Attendance Table
            </button>
          </motion.div>
        )}
      </main>

      {/* MODAL */}
      <AnimatePresence>
        {showModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/70 backdrop-blur-md z-50 flex items-center justify-center"
          >
            <motion.div
              initial={{ scale: 0.8 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.8 }}
              className="bg-neutral-900 p-8 rounded-3xl border border-white/10 shadow-xl max-w-lg w-full"
            >
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Icons.Table />
                Attendance Table
              </h3>

              <div className="space-y-3 max-h-96 overflow-auto p-2">
                {results.map((item, i) => {
                  const name = Object.keys(item)[0];
                  const score = Object.values(item)[0];

                  return (
                    <div
                      key={i}
                      className="flex justify-between p-3 bg-neutral-800/50 rounded-xl border border-neutral-700"
                    >
                      <span className="text-white font-medium">{name}</span>
                      <span className={`${confidenceColor(score)} font-mono text-lg`}>
                        {(score * 100).toFixed(2)}%
                      </span>
                    </div>
                  );
                })}
              </div>

              <button
                onClick={() => setShowModal(false)}
                className="w-full mt-6 py-3 bg-red-600 hover:bg-red-700 rounded-xl font-semibold flex items-center justify-center gap-2"
              >
                <Icons.X className="w-5 h-5" /> Close
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
