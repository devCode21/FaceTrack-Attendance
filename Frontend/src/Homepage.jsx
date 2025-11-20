// ⚡ Ultra-Professional Home Page — Fixed JSX, Completed CTA, Clean Structure
// Dark enterprise theme, accessible markup, motion, and fully closed tags.

import React from "react";
import { motion } from "framer-motion";
import * as Icons from "lucide-react";

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  show: { opacity: 1, y: 0 },
};

const FeatureCard = ({ icon: Icon, title, description }) => (
  <motion.div
    variants={fadeUp}
    className="p-6 rounded-2xl bg-zinc-900/60 backdrop-blur-xl border border-zinc-800 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
  >
    <div className="p-3 w-fit rounded-xl bg-zinc-800/70 border border-zinc-700 shadow-inner">
      <Icon className="w-6 h-6 text-neutral-200" />
    </div>
    <h4 className="font-semibold text-neutral-100 mt-4 text-lg tracking-tight">{title}</h4>
    <p className="text-sm text-neutral-400 mt-1 leading-relaxed">{description}</p>
  </motion.div>
);

export default function Home() {
  const features = [
    { icon: Icons.Camera, title: "YOLO Face Detection", description: "Real‑time classroom detection with low latency." },
    { icon: Icons.Fingerprint, title: "ResNet Recognition", description: "Robust embeddings for identity matching." },
    { icon: Icons.Clock, title: "Automated Marking", description: "Attendance logged automatically from video." },
    { icon: Icons.FileText, title: "Audit‑Ready Reports", description: "CSV exports for audit & analytics." },
    { icon: Icons.Layers3, title: "Face Alignment (MTCNN)", description: "Accurate alignment to boost recognition." },
    { icon: Icons.Database, title: "MongoDB Storage", description: "Secure, scalable persistence for records." },
  ];

  return (
    <div className="min-h-screen bg-black text-neutral-200 font-sans relative overflow-hidden">
      {/* Background Glow Effects */}
      <div className="absolute -left-10 -top-10 w-80 h-80 bg-sky-600/8 blur-3xl rounded-full pointer-events-none" aria-hidden="true" />
      <div className="absolute -right-20 -bottom-20 w-96 h-96 bg-purple-600/8 blur-3xl rounded-full pointer-events-none" aria-hidden="true" />

      {/* NAVBAR */}
      <header className="fixed top-0 w-full bg-black/40 backdrop-blur-xl border-b border-zinc-800 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-zinc-700 to-black border border-zinc-600 flex items-center justify-center font-bold text-white shadow-lg">FR</div>
            <div>
              <h1 className="text-xl font-semibold tracking-tight text-white">FaceRec</h1>
              <p className="text-xs text-neutral-400 -mt-0.5">AI Attendance System</p>
            </div>
          </div>

          <nav className="flex items-center gap-3">
            <a
              href="#"
              className="hidden sm:block px-4 py-2 rounded-lg border border-zinc-700 bg-zinc-900/40 text-neutral-300 hover:bg-zinc-800 transition text-sm"
            >
              Student Panel
            </a>
            <a
              href="#"
              className="px-5 py-2 rounded-lg bg-sky-600 text-white text-sm font-medium hover:bg-sky-700 transition shadow-md"
            >
              Teacher Login
            </a>
          </nav>
        </div>
      </header>

      {/* MAIN */}
      <main className="max-w-7xl mx-auto px-6 pt-36 pb-24">
        {/* HERO */}
        <motion.section initial="hidden" animate="show" transition={{ staggerChildren: 0.08 }} className="text-left max-w-4xl">
          <motion.h1 variants={fadeUp} className="text-5xl md:text-6xl font-bold tracking-tight text-white leading-tight">
            AI‑Powered <span className="text-sky-400">Attendance</span> for Modern Classrooms
          </motion.h1>

          <motion.p variants={fadeUp} className="mt-4 text-lg text-neutral-400 max-w-2xl leading-relaxed">
            Built with <strong>YOLO</strong>, <strong>MTCNN</strong>, and <strong>ResNet</strong> — reliable recognition in real-world conditions.
          </motion.p>

          <motion.div variants={fadeUp} className="mt-8 flex gap-4">
            <a href="#" className="px-8 py-3 rounded-xl bg-sky-600 text-white text-lg font-semibold shadow-lg hover:bg-sky-700 hover:scale-[1.02] transition inline-flex items-center gap-2">
              <Icons.PlayCircle className="w-5 h-5" /> Start Recognition
            </a>
            <a href="#learn-more" className="px-6 py-3 rounded-xl border border-zinc-700 text-neutral-300 hover:bg-zinc-900/40 transition inline-flex items-center gap-2">
              Learn More <Icons.CornerDownRight className="w-4 h-4" />
            </a>
          </motion.div>
        </motion.section>

        {/* HIGHLIGHTS */}
        <div className="mt-10 flex flex-wrap gap-6 text-neutral-400 text-sm">
          <div className="flex items-center gap-2"><Icons.Cpu className="w-4 h-4 text-sky-400" /> YOLO + MTCNN + ResNet</div>
          <div className="flex items-center gap-2"><Icons.CheckCircle className="w-4 h-4 text-green-500" /> Auto Attendance</div>
          <div className="flex items-center gap-2"><Icons.Download className="w-4 h-4 text-neutral-400" /> CSV Exports</div>
        </div>

        {/* FEATURES GRID */}
        <section className="mt-16">
          <motion.h2 variants={fadeUp} initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.2 }} className="text-3xl font-bold text-center text-white">
            Production‑Grade Pipeline
          </motion.h2>

          <motion.p variants={fadeUp} initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.2 }} className="text-center text-neutral-400 max-w-2xl mx-auto mt-3">
            Optimized for throughput, accuracy, and fault tolerance — ready for institutions.
          </motion.p>

          <motion.div initial="hidden" whileInView="show" transition={{ staggerChildren: 0.08 }} viewport={{ once: true, amount: 0.2 }} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-10">
            {features.map((f, i) => (
              <FeatureCard key={i} {...f} />
            ))}
          </motion.div>
        </section>

        {/* CTA */}
        <section className="mt-20 bg-zinc-900/60 backdrop-blur-xl border border-zinc-800 rounded-3xl p-8 md:p-10 shadow-xl shadow-black/40">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="max-w-2xl">
              <h3 className="text-2xl md:text-3xl font-bold text-white">Automate Attendance Effortlessly</h3>
              <p className="text-neutral-400 mt-2">Onboard your institution, upload classes, and let AI handle the rest.</p>
            </div>

            <div className="flex gap-4">
              <a href="#signup" className="px-6 py-3 rounded-xl bg-sky-600 text-white font-semibold hover:bg-sky-700 transition shadow-md inline-flex items-center gap-2">Teacher Sign Up <Icons.ArrowRight className="w-4 h-4" /></a>
              <a href="#docs" className="px-6 py-3 rounded-xl border border-zinc-700 text-neutral-300 hover:bg-zinc-900/40 transition inline-flex items-center gap-2">View Docs <Icons.FileText className="w-4 h-4" /></a>
            </div>
          </div>
        </section>
      </main>

      {/* FOOTER */}
      <footer className="border-t border-zinc-800 bg-black/80"> 
        <div className="max-w-7xl mx-auto px-6 py-6 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-neutral-500">© {new Date().getFullYear()} FaceRec. All rights reserved.</p>
          <div className="text-sm text-neutral-500 font-medium space-x-3">
            <span>YOLO</span>
            <span>MTCNN</span>
            <span>ResNet</span>
            <span>MongoDB</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
