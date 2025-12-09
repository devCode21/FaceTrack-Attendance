import React from "react";
import { createRoot } from 'react-dom/client';
import './index.css';
import { BrowserRouter } from "react-router-dom";
import Homepage from './Homepage.jsx';
import CourseEntryForm from './TeacherSignup.jsx';
import CreativeAttendancePage from './videoUploadPage.jsx';
import { Routes, Route } from "react-router-dom";
import store from '../components/state.js';
import { Provider, useSelector } from "react-redux";
import CourseLoginForm from './Loginpage.jsx';
import AttendancePage from './attendance_page.jsx';
import { useDispatch } from "react-redux";
import { Login_data , add_course_info , add_form, add_student_name  } from "../components/state.js";
function App() {
   const dispatch = useDispatch();
  // Load data FROM localStorage at startup
  const [state , setState] = React.useState(() => {
    const stored = localStorage.getItem("state");
    return stored ? JSON.parse(stored) : null;
  });
  console.log(state)
  if (state){
         dispatch(Login_data());
         dispatch(add_form({"formdata":state.formdata}))
         dispatch(add_course_info({"CourseID":state.CourseID }))
         dispatch(add_student_name({"student_name":state.students}))
  }

  const Login = useSelector((state) => state.Data.Login);

   


  return (
    <Routes>
      <Route path='/' element={<Homepage Login={Login} />} />
      <Route path="/teacher-signup" element={<CourseEntryForm  />} />
      <Route path="/dashboard" element={<CreativeAttendancePage />} />
      <Route path="/teacher-login" element={<CourseLoginForm />} />
      <Route path='/attendance-page' element={<AttendancePage />} />
    </Routes>
  );
}


createRoot(document.getElementById("root")).render(
  <Provider store={store}>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </Provider>
);
