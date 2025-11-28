import React, { useState } from "react";
import { motion } from "framer-motion";
import { BookOpen, User, Lock, ArrowRight, CornerDownRight, Check, X } from "lucide-react";
import axios from "axios";
import { useNavigate } from "react-router";
import { Get_course_id_sigin_API } from "./backendAPI";
import { Login_data , add_course_info , add_form } from "./state";
import { useDispatch , useSelector } from "react-redux";
import {
  Card,
  CardContent,
  CardHeader,
  CardDescription,
  CardTitle,
  Button,
  LabeledInput
} from "../components/card_componets";


// =============================
// BEST TOAST SYSTEM (GLOBAL)
// =============================
const useToast = () => {
  return {
    toast: ({ title, description, status }) => {
      const color =
        status === "success"
          ? "bg-green-600"
          : status === "error"
          ? "bg-red-600"
          : "bg-gray-700";

      const icon =
        status === "success"
          ? `<svg class='w-5 h-5' fill='none' stroke='white' stroke-width='2' viewBox='0 0 24 24'><path d='M5 13l4 4L19 7'/></svg>`
          : status === "error"
          ? `<svg class='w-5 h-5' fill='none' stroke='white' stroke-width='2' viewBox='0 0 24 24'><path d='M6 18L18 6M6 6l12 12'/></svg>`
          : "";

      const el = document.createElement("div");
      el.className = `
        fixed top-6 right-6 px-4 py-3 rounded-xl text-white shadow-2xl 
        flex items-start gap-3 animate-toast-in ${color} z-[9999]
      `;

      el.innerHTML = `
        <div>${icon}</div>
        <div>
          <strong class="text-sm">${title}</strong>
          <p class="text-xs opacity-90 mt-0.5">${description || ""}</p>
        </div>
      `;

      document.body.appendChild(el);

      setTimeout(() => {
        el.classList.add("animate-toast-out");
        setTimeout(() => el.remove(), 300);
      }, 2500);
    }
  };
};


// =============================
// CSS (Add to index.css)
// =============================
/*

@keyframes toastIn {
  from { opacity: 0; transform: translateY(-10px) scale(0.95); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes toastOut {
  from { opacity: 1; transform: translateY(0) scale(1); }
  to   { opacity: 0; transform: translateY(-10px) scale(0.95); }
}

.animate-toast-in { animation: toastIn 0.25s ease-out forwards; }
.animate-toast-out { animation: toastOut 0.25s ease-in forwards; }

*/


// =============================
// MAIN COMPONENT
// =============================
export default function CourseEntryForm() {
  const dispatch =useDispatch()
  
  const navigate = useNavigate();
  const { toast } = useToast();

  const [form, setForm] = useState({
    class: "",
    course_name: "",
    teacher_name: "",
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
    if (!form.class.trim()) newErrors.class = "Class is required.";
    if (!form.course_name.trim()) newErrors.course_name = "Course Name is required.";
    if (!form.teacher_name.trim()) newErrors.teacher_name = "Teacher Name is required.";
    if (form.password.length < 4) newErrors.password = "Minimum 4 characters required.";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setLoading(true);

    const payload = {
      course_name: form.course_name,
      teacher_name: form.teacher_name,
      class_name: form.class,
      password: form.password,
    };

    try {
      const respone =await axios.post(Get_course_id_sigin_API, payload);
      console.log(respone.data.data.Course_id)

      toast({
        title: "Verification Successful",
        description: "Course verified successfully.",
        status: "success",
      });

      dispatch(Login_data());
      dispatch(add_form({"formdata":payload}))
      dispatch(add_course_info({"CourseID":respone.data.data.Course_id }))
      setLoading(false);
      navigate("/dashboard");

    } catch (err) {
      console.log(err)
      toast({
        title: "Verification Failed",
        description: err.response.data.message,
        status: "error",
      });

      setLoading(false);
    }
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 50, scale: 0.95 },
    visible: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: { duration: 0.6, ease: "easeOut" },
    },
  };

  return (
    <div
      className="
      min-h-screen flex flex-col items-center justify-center 
      bg-gradient-to-br from-gray-900 via-black to-gray-900 
      p-4 sm:p-6 relative overflow-hidden
    "
    >
      {/* Background Glow */}
      <div className="absolute top-10 left-10 w-52 h-52 sm:w-60 sm:h-60 bg-blue-500/20 blur-[80px] rounded-full" />
      <div className="absolute bottom-10 right-10 w-60 h-60 sm:w-72 sm:h-72 bg-purple-500/20 blur-[80px] rounded-full" />

      <motion.div
        variants={cardVariants}
        initial="hidden"
        animate="visible"
        className="w-full max-w-md px-2"
      >
        <Card className="shadow-2xl border border-gray-700 bg-black/40 backdrop-blur-xl rounded-2xl">
          <CardHeader className="space-y-2 text-center">

            {/* Tag */}
            <div
              className="
              mx-auto mb-2 inline-flex items-center gap-2 px-3 py-1 rounded-full
              bg-gray-800 border border-gray-700 text-gray-300 text-xs uppercase tracking-widest
            "
            >
              <span className="h-2 w-2 bg-blue-400 rounded-full" />
              Secure Access
            </div>

            <CardTitle className="text-2xl font-semibold text-white">
              Course Enrollment
            </CardTitle>
            <CardDescription className="text-gray-400 text-sm">
              Enter your course details to begin automated attendance
            </CardDescription>
          </CardHeader>

          <CardContent className="px-4 sm:px-6">
            <form onSubmit={handleSubmit} className="space-y-5">

              <LabeledInput
                Icon={CornerDownRight}
                label="Class"
                id="class"
                placeholder="e.g., CSE-301"
                value={form.class}
                onChange={handleChange}
                error={errors.class}
              />

              <LabeledInput
                Icon={BookOpen}
                label="Course Name"
                id="course_name"
                placeholder="Advanced Machine Learning"
                value={form.course_name}
                onChange={handleChange}
                error={errors.course_name}
              />

              <LabeledInput
                Icon={User}
                label="Teacher Name"
                id="teacher_name"
                placeholder="Dr. John Doe"
                value={form.teacher_name}
                onChange={handleChange}
                error={errors.teacher_name}
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

              <p className="text-gray-500 text-xs text-center -mt-2">
                Your details are encrypted & secure
              </p>

              <Button
                type="submit"
                disabled={loading}
                className="w-full flex items-center justify-center gap-2 mt-4"
              >
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
