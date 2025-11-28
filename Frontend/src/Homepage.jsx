import React from "react";
import { motion } from "framer-motion";
import * as Icons from "lucide-react";
import { Link, NavLink } from "react-router-dom";
import { FeatureCard, fadeUp } from "../components/card_componets";

export default function Home() {
  const features = [
    { icon: Icons.Camera, title: "YOLO Face Detection", description: "Real-time classroom detection with low latency." },
    { icon: Icons.Fingerprint, title: "ResNet Recognition", description: "Robust embeddings for identity matching." },
    { icon: Icons.Clock, title: "Automated Marking", description: "Attendance logged automatically from video." },
    { icon: Icons.FileText, title: "Audit-Ready Reports", description: "CSV exports for audit & analytics." },
    { icon: Icons.Layers3, title: "Face Alignment (MTCNN)", description: "Accurate alignment to boost recognition." },
    { icon: Icons.Database, title: "MongoDB Storage", description: "Secure, scalable persistence for records." },
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.7, ease: "easeOut" }}
      className="min-h-screen bg-black text-neutral-200 font-sans relative overflow-hidden"
    >
      {/* Background Glow */}
      <div className="absolute -left-10 -top-10 w-80 h-80 bg-sky-600/20 blur-3xl rounded-full pointer-events-none" />
      <div className="absolute -right-20 -bottom-20 w-96 h-96 bg-purple-600/20 blur-3xl rounded-full pointer-events-none" />

      {/* NAVBAR */}
      <header className="fixed top-0 w-full bg-black/40 backdrop-blur-xl border-b border-zinc-800 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
          
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-zinc-700 to-black border border-zinc-600 flex items-center justify-center font-bold text-white shadow-lg">
              FR
            </div>
            <div>
              <h1 className="text-xl font-semibold text-white">FaceRec</h1>
              <p className="text-xs text-neutral-400 -mt-1">AI Attendance System</p>
            </div>
          </div>

          {/* Desktop Nav */}
          <nav className="hidden sm:flex items-center gap-4">
            <NavLink
              to="/student"
              className={({ isActive }) =>
                `px-4 py-2 rounded-lg border text-sm transition ${
                  isActive
                    ? "bg-zinc-800 text-white border-zinc-700"
                    : "bg-zinc-900/40 text-neutral-300 border-zinc-700 hover:bg-zinc-800"
                }`
              }
            >
              Student Panel
            </NavLink>

            <NavLink
              to="/teacher-login"
              className={({ isActive }) =>
                `px-5 py-2 rounded-lg text-sm font-medium transition shadow-md ${
                  isActive
                    ? "bg-sky-600 text-white"
                    : "bg-sky-600/90 hover:bg-sky-700 text-white"
                }`
              }
            >
              Teacher Login
            </NavLink>
          </nav>

          {/* Mobile Button */}
          <NavLink
            to="/teacher-login"
            className="sm:hidden px-4 py-1.5 rounded-lg bg-sky-600 text-white text-xs font-medium"
          >
            Login
          </NavLink>
        </div>
      </header>

      {/* MAIN */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 pt-32 sm:pt-36 pb-24">

        {/* HERO SECTION */}
        <motion.section
          initial="hidden"
          animate="show"
          transition={{ staggerChildren: 0.08 }}
          className="relative text-left max-w-4xl"
        >
          {/* Futuristic Gradient Glow */}
          <div className="absolute -right-12 top-10 w-72 sm:w-96 aspect-square rounded-full 
                          bg-gradient-to-br from-sky-500/20 via-purple-500/20 to-pink-500/20 
                          blur-3xl animate-pulse opacity-60 pointer-events-none" />

          <div className="absolute -right-4 top-28 w-40 sm:w-56 aspect-square rounded-full 
                          bg-sky-300/10 blur-2xl animate-spin-slow pointer-events-none" />

          {/* Hero Title */}
          <motion.h1
            variants={fadeUp}
            className="text-4xl sm:text-5xl md:text-6xl font-bold tracking-tight text-white leading-tight"
          >
            AI-Powered <span className="text-sky-400">Attendance</span> 
            <br className="hidden sm:block" />
            for Modern Classrooms
          </motion.h1>

          {/* Hero Subtitle */}
          <motion.p
            variants={fadeUp}
            className="mt-4 text-base sm:text-lg text-neutral-400 max-w-2xl leading-relaxed"
          >
            Built using <strong>YOLO</strong>, <strong>MTCNN</strong>, and <strong>ResNet</strong>.
            Accurate. Automated. Reliable even in real-world conditions.
          </motion.p>

          {/* CTAs */}
          <motion.div variants={fadeUp} className="mt-8 flex flex-col sm:flex-row gap-3 sm:gap-4">

            {/* Teacher Login */}
            <Link
              to="/teacher-login"
              className="px-6 py-3 rounded-xl bg-sky-600 text-white text-lg font-semibold shadow-lg 
                         hover:bg-sky-700 hover:-translate-y-1 active:scale-95 transition inline-flex 
                         items-center gap-2 justify-center"
            >
              <Icons.LogIn className="w-5 h-5" />
              Login as Teacher
            </Link>

            {/* Learn More → GitHub README */}
            <a
              href="#"
              target="_blank"
              rel="noopener noreferrer"
              className="px-6 py-3 rounded-xl bg-green-500/20 border border-green-500/40 text-white 
                         text-lg font-semibold hover:bg-green-600/30 hover:-translate-y-1 active:scale-95 
                         transition inline-flex items-center gap-2 justify-center"
            >
              <Icons.BookOpen className="w-5 h-5" />
              Learn More
            </a>

          </motion.div>
        </motion.section>

        {/* HIGHLIGHTS */}
        <div className="mt-10 flex flex-col sm:flex-row flex-wrap gap-4 sm:gap-6 text-neutral-400 text-sm">
          <div className="flex items-center gap-2">
            <Icons.Cpu className="w-4 h-4 text-sky-400" /> YOLO + MTCNN + ResNet
          </div>
          <div className="flex items-center gap-2">
            <Icons.CheckCircle className="w-4 h-4 text-green-500" /> Automated Attendance
          </div>
          <div className="flex items-center gap-2">
            <Icons.Download className="w-4 h-4 text-purple-400" /> CSV Export Support
          </div>
        </div>

        {/* FEATURES GRID */}
        <section className="mt-16">
          <motion.h2
            variants={fadeUp}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.25 }}
            className="text-3xl font-bold text-center text-white"
          >
            Production-Grade Pipeline
          </motion.h2>

          <motion.p
            variants={fadeUp}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.25 }}
            className="text-center text-neutral-400 max-w-2xl mx-auto mt-3 text-base"
          >
            Optimized for throughput, accuracy, scaling and fault tolerance — ready for deployment.
          </motion.p>

          <motion.div
            initial="hidden"
            whileInView="show"
            transition={{ staggerChildren: 0.08 }}
            viewport={{ once: true, amount: 0.25 }}
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-10"
          >
            {features.map((f, i) => (
              <FeatureCard key={i} {...f} />
            ))}
          </motion.div>
        </section>

        {/* FINAL CTA */}
        <section className="mt-20 bg-zinc-900/60 backdrop-blur-xl border border-zinc-800 rounded-3xl p-10 shadow-xl shadow-black/40 relative overflow-hidden">

          {/* Glow Inside Box */}
          <div className="absolute inset-0 bg-gradient-to-br from-sky-600/10 to-purple-600/10 opacity-20 pointer-events-none" />

          <div className="relative flex flex-col md:flex-row items-center justify-between gap-6 text-center md:text-left">

            <div className="max-w-2xl">
              <h3 className="text-3xl font-bold text-white">
                Automate Attendance Effortlessly
              </h3>
              <p className="text-neutral-400 mt-3 text-base">
                Onboard your class, upload your session data — and let AI handle everything.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">

              <Link
                to="/teacher-login"
                className="px-6 py-3 rounded-xl bg-sky-600 text-white font-semibold 
                           hover:bg-sky-700 hover:-translate-y-1 active:scale-95 transition 
                           shadow-md inline-flex items-center justify-center gap-2"
              >
                Teacher Sign Up <Icons.ArrowRight className="w-4 h-4" />
              </Link>

              <Link
                to="/docs"
                className="px-6 py-3 rounded-xl border border-zinc-700 text-neutral-300 
                           hover:bg-zinc-900/40 transition inline-flex items-center justify-center gap-2"
              >
                View Docs <Icons.FileText className="w-4 h-4" />
              </Link>

            </div>
          </div>
        </section>
      </main>

      {/* FOOTER */}
      <footer className="border-t border-zinc-800 bg-black/80 mt-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 flex flex-col md:flex-row items-center justify-between gap-4 text-center md:text-left">
          <p className="text-sm text-neutral-500">
            © {new Date().getFullYear()} FaceRec. All rights reserved.
          </p>

          <div className="text-sm text-neutral-500 font-medium space-x-3">
            <span>YOLO</span>
            <span>MTCNN</span>
            <span>ResNet</span>
            <span>MongoDB</span>
          </div>
        </div>
      </footer>
    </motion.div>
  );
}
