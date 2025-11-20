import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Homepage from './Homepage.jsx'
import CourseEntryForm from './TeacherLogin.jsx'
import TeacherAttendanceDashboard from './videoUploadPage.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <CourseEntryForm/>
  </StrictMode>,
)
