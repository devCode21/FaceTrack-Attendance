
import { createSlice } from "@reduxjs/toolkit";
import { configureStore } from "@reduxjs/toolkit";
const initialState={
   
    Login:false,
    formdata: null,
    CourseID: null
  
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

     Login_data:(state)=>{
            if (state['Login']==true){
                return initialState  
            }
            else {
                state['Login']=true
            }
     }

  }
});

export const { add_form, add_course_info,Login_data , } = Form_Data.actions;


const store = configureStore({
  reducer: {
    Data: Form_Data.reducer,
  },
});



export default store;