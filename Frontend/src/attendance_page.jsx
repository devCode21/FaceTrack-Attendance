// AttendancePage.jsx — Ultra Professional Version (No USN)
import React, { use } from "react";
import { motion } from "framer-motion";
import * as Icons from "lucide-react";
import { useSelector } from "react-redux";

export default function AttendancePage() {
  // Dummy Data
  const selector = useSelector((state) => state.Data);
  const className = useSelector((state) => state.Data.formdata.class_name) || "Data Structures";
  const courseName = (useSelector((state) => state.Data.formdata.course_name) || "CS101");

  const students = [
    { name: "Aarav Sharma", present: true },
    { name: "Riya Patel", present: false },
    { name: "Kabir Mehta", present: true },
    { name: "Ananya Rao", present: true },
    { name: "Yash Verma", present: false },
  ];

  return (
    <div className="min-h-screen bg-[#050505] text-neutral-200 p-6 relative overflow-hidden font-sans">

      {/* Soft Gradient Glow Background */}
      <div className="absolute -left-32 top-0 w-[36rem] h-[36rem] bg-sky-500/20 blur-[160px] rounded-full" />
      <div className="absolute right-0 top-40 w-[40rem] h-[40rem] bg-purple-600/25 blur-[170px] rounded-full" />
      <div className="absolute left-1/2 bottom-0 -translate-x-1/2 w-[28rem] h-[28rem] bg-indigo-500/10 blur-[140px] rounded-full" />

      {/* PAGE HEADER */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-6xl mx-auto mt-14 mb-10"
      >
        <h1 className="text-5xl font-bold tracking-tight text-white drop-shadow-[0_0_18px_rgba(255,255,255,0.25)]">
          Attendance Dashboard
        </h1>
        <p className="text-neutral-400 mt-2 text-sm">AI‑powered automated attendance overview</p>
      </motion.div>

      {/* CLASS INFO CARD */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="max-w-6xl mx-auto bg-zinc-900/60 backdrop-blur-2xl border border-zinc-800 rounded-3xl px-8 py-6 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6"
      >
        <div>
          <h2 className="text-3xl font-semibold text-white">{className}</h2>
          <h3 className="text-lg text-neutral-300 mt-1">
            Course: <span className="text-sky-400 font-semibold">{courseName}</span>
          </h3>
        </div>

        <button
          className="px-6 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-700 transition text-white font-medium flex items-center gap-2 shadow-lg border border-sky-400/30 hover:shadow-[0_0_20px_rgba(56,189,248,0.45)]"
        >
          <Icons.Play className="w-4 h-4" /> Play Session Video
        </button>
      </motion.div>

      {/* STUDENTS TABLE */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="max-w-6xl mx-auto mt-10 overflow-x-auto"
      >
        <table className="w-full border-collapse bg-zinc-900/60 backdrop-blur-xl border border-zinc-800 rounded-2xl shadow-[0_0_30px_rgba(0,0,0,0.35)] overflow-hidden">
          <thead className="bg-gradient-to-r from-zinc-900 to-zinc-800 text-neutral-300 text-xs uppercase tracking-wide">
            <tr>
              <th className="py-4 px-5 font-semibold text-left">#</th>
              <th className="py-4 px-5 font-semibold text-left">Student Name</th>
              <th className="py-4 px-5 font-semibold text-center">Status</th>
            </tr>
          </thead>

          <tbody>
            {students.map((s, i) => (
              <tr
                key={i}
                className="border-t border-zinc-800 hover:bg-zinc-800/40 transition-colors duration-200"
              >
                <td className="py-4 px-5 text-neutral-500 text-sm">{i + 1}</td>
                <td className="py-4 px-5 text-white font-medium tracking-tight">{s.name}</td>

                <td className="py-4 px-5 text-center">
                  {s.present ? (
                    <span className="px-4 py-1.5 rounded-full bg-green-500/20 text-green-300 border border-green-500/30 text-sm font-semibold flex items-center justify-center gap-2 w-fit mx-auto">
                      <Icons.CheckCircle className="w-4 h-4" /> Present
                    </span>
                  ) : (
                    <span className="px-4 py-1.5 rounded-full bg-red-500/20 text-red-300 border border-red-500/30 text-sm font-semibold flex items-center justify-center gap-2 w-fit mx-auto">
                      <Icons.XCircle className="w-4 h-4" /> Absent
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </motion.div>
    </div>
  );
}
