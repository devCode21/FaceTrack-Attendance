import React, { useState } from "react";
import { motion } from "framer-motion";
import { BookOpen, User, Lock, ArrowRight } from "lucide-react";
import axios from "axios";
import { useNavigate } from "react-router";
import { Get_course_id_Login_API } from "../components/BackendApi.js";
import { Login_data, add_course_info, add_form } from "../components/state.js";
import { useDispatch } from "react-redux";
import {
  Card,
  CardContent,
  CardHeader,
  CardDescription,
  CardTitle,
  Button,
  LabeledInput,
} from "../components/card_componets.jsx";

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
    },
  };
};

export default function CourseLoginForm() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { toast } = useToast();

  const [form, setForm] = useState({
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

    if (!form.course_name.trim()) newErrors.course_name = "Course Name is required.";
    if (!form.teacher_name.trim()) newErrors.teacher_name = "Teacher Name is required.";
    if (form.password.length < 4) newErrors.password = "Minimum 4 characters required.";
    if (form.password !== form.confirm_password)
      newErrors.confirm_password = "Passwords do not match.";

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
      password: form.password,
    };

    try {
      const response = await axios.post(Get_course_id_Login_API, payload);

      toast({
        title: "Verification Successful",
        description: "Course verified successfully.",
        status: "success",
      });

      dispatch(Login_data());
      dispatch(add_form({ formdata: payload }));
      dispatch(add_course_info({ CourseID: response.data.data.Course_id }));

      setLoading(false);
      navigate("/dashboard");
    } catch (err) {
      toast({
        title: "Verification Failed",
        description: err?.response?.data?.message || "Something went wrong.",
        status: "error",
      });
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 via-black to-gray-900 p-4 sm:p-6 relative overflow-hidden">

      <div className="absolute top-16 left-16 w-64 h-64 bg-blue-500/20 blur-[110px] rounded-full" />
      <div className="absolute bottom-16 right-16 w-64 h-64 bg-purple-500/20 blur-[110px] rounded-full" />

      <motion.div
        initial={{ opacity: 0, y: 60, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.7, ease: "easeOut" }}
        className="w-full max-w-md px-2"
      >
        <Card className="shadow-2xl border border-gray-700/60 bg-black/40 backdrop-blur-xl rounded-2xl hover:bg-black/50 transition-all duration-300">
          <CardHeader className="space-y-2 text-center">

            <div className="mx-auto mb-2 inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-800/60 border border-gray-700 text-gray-300 text-xs uppercase tracking-widest">
              <span className="h-2 w-2 bg-blue-400 rounded-full" />
              Secure Access
            </div>

            <CardTitle className="text-2xl font-bold text-white tracking-wide">
              Course Enrollment
            </CardTitle>

            <CardDescription className="text-gray-400 text-sm tracking-wide">
              Enter your details to continue
            </CardDescription>
          </CardHeader>

          <CardContent className="px-4 sm:px-6">

            <form onSubmit={handleSubmit} className="space-y-5">

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

              <LabeledInput
                Icon={Lock}
                label="Confirm Password"
                id="confirm_password"
                type="password"
                placeholder="Re-enter password"
                value={form.confirm_password}
                onChange={handleChange}
                error={errors.confirm_password}
              />

              <div className="pt-1 w-full flex justify-start pl-1">
                <button
                  type="button"
                  onClick={() => navigate("/teacher-signup")}
                  className="text-xs text-gray-400 hover:text-gray-200 underline underline-offset-2 transition"
                >
                  Don’t have an account? Sign up
                </button>
              </div>

              <Button
                type="submit"
                disabled={loading}
                className="w-full flex items-center justify-center gap-2 mt-3 rounded-xl bg-blue-600 hover:bg-blue-700 transition-all"
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
