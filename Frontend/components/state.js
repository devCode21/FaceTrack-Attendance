
import { createSlice } from "@reduxjs/toolkit";
import { configureStore } from "@reduxjs/toolkit";
const initialState={
   
    Login:false,
    formdata: null,
    CourseID: null, 
    students: null
  
}
const Form_Data = createSlice({
    name: "Data" ,
    initialState,
  reducers: {
     add_form:(state , action)=>{
        state["formdata"]=action.payload.formdata
     },

     add_course_info :(state , action)=>{
        state['CourseID'] =action.payload.CourseID
     } , 

     add_student_name:(state , action )=>{
      state['students']=action.payload.student_name
     },

     Login_data:(state)=>{
            if (state['Login']==true){
                return initialState  
            }
            else {
                state['Login']=true
            }
     }
,
     store_data :(state)=>{
       localStorage.setItem("state" , JSON.stringify(state))
     }

  }
});

export const { add_form, add_course_info,Login_data ,store_data ,add_student_name } = Form_Data.actions;


const store = configureStore({
  reducer: {
    Data: Form_Data.reducer,
  },
});



export default store;