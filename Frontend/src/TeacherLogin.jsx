import React, { useState } from "react";
import { motion } from "framer-motion";
import { BookOpen, User, Lock, ArrowRight, CornerDownRight } from "lucide-react";

import { Card , CardContent ,CardHeader,CardDescription,CardTitle ,Button ,Input ,LabeledInput } from "../components/card_componets";

const useToast = () => ({ toast: ({ title }) => console.log("TOAST:", title) });
const Toaster = () => null;
// ======================= MAIN COMPONENT ================================
export default function CourseEntryForm() {
  const { toast } = useToast();

  const [form, setForm] = useState({
    class: "",
    className: "",
    teacherName: "",
    password: "",
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.id]: e.target.value });
    setErrors({ ...errors, [e.target.id]: "" });
  };

  const validate = () => {
    let newErrors = {};
    if (!form.class.trim()) newErrors.class = "Class ID is required.";
    if (!form.className.trim()) newErrors.className = "Class Name is required.";
    if (!form.teacherName.trim()) newErrors.teacherName = "Teacher Name is required.";
    if (form.password.length < 4) newErrors.password = "Minimum 4 characters required.";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;

    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      toast({ title: "Verification successful" });
      console.log("Navigating with data:", form);
    }, 1200);
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 60, scale: 0.95 },
    visible: { opacity: 1, y: 0, scale: 1, transition: { duration: 0.6, ease: "easeOut" } },
  };

  return (
    <div className="min-h-screen flex flex-col gap-10 justify-center items-center bg-gradient-to-br from-black via-zinc-900 to-black p-6 relative overflow-hidden">

      {/* Decorative Background Glows */}
      <div className="absolute top-10 left-10 w-52 h-52 bg-sky-500/10 blur-3xl rounded-full" aria-hidden />
      <div className="absolute bottom-10 right-10 w-64 h-64 bg-purple-500/10 blur-[90px] rounded-full" aria-hidden />

      <Toaster />

      <motion.div variants={cardVariants} initial="hidden" animate="visible" className="w-full flex justify-center">
        <Card className="shadow-[0_0_45px_rgba(0,0,0,0.55)] border-zinc-700 backdrop-blur-2xl">
          <CardHeader>
            {/* Top badge */}
            <div className="mb-3 inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-800 border border-zinc-700 text-neutral-300 text-xs uppercase tracking-wide w-fit">
              <span className="h-2 w-2 bg-sky-400 rounded-full" />
              Secure Access Portal
            </div>

            <CardTitle>Course Enrollment</CardTitle>
            <CardDescription>Enter course details to begin automated attendance.</CardDescription>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-5">
              <LabeledInput
                Icon={CornerDownRight}
                label="Class ID"
                id="class"
                placeholder="e.g., CSC 401"
                value={form.class}
                onChange={handleChange}
                error={errors.class}
              />

              <LabeledInput
                Icon={BookOpen}
                label="Class Name"
                id="className"
                placeholder="Advanced ML"
                value={form.className}
                onChange={handleChange}
                error={errors.className}
              />

              <LabeledInput
                Icon={User}
                label="Teacher Name"
                id="teacherName"
                placeholder="Dr. Jane Doe"
                value={form.teacherName}
                onChange={handleChange}
                error={errors.teacherName}
              />

              <LabeledInput
                Icon={Lock}
                label="Password"
                id="password"
                type="password"
                placeholder="Minimum 4 characters"
                value={form.password}
                onChange={handleChange}
                error={errors.password}
              />

              {/* Helper Note */}
              <p className="text-neutral-500 text-xs text-center -mt-2">Your details are encrypted & secure</p>

              <Button type="submit" disabled={loading} className="w-full flex items-center gap-2 mt-6">
                {loading ? (
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                ) : (
                  <ArrowRight className="h-4 w-4" />
                )}
                {loading ? "Verifying..." : "Verify & Continue"}
              </Button>
            </form>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
