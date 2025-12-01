import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import {BrowserRouter} from "react-router-dom"
import Homepage from './Homepage.jsx'
import CourseEntryForm from './TeacherSignup.jsx'
import CreativeAttendancePage from './videoUploadPage.jsx'
import { Routes, Route } from "react-router-dom";
import store from '../components/state.js'
import { Provider } from "react-redux";



createRoot(document.getElementById("root")).render(
 <Provider store={store}>
      <BrowserRouter >
  <Routes>
   
      <Route path='/' element={<Homepage />} />
      <Route path="/teacher-login" element={<CourseEntryForm />} />
      <Route path="/dashboard" element={<CreativeAttendancePage />} />
    
   
  </Routes>
</BrowserRouter>
  

 </Provider>
);