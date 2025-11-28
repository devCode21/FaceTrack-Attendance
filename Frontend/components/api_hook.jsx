// import { useEffect, useState } from "react"
// import axios from "axios"
// import { data } from "react-router"


// const useCallAPI =(API_LINK , method , Data)=>{
//     const  [res , setRes]=useState({})
//     useEffect=(()=>{
    
//       const get_data=async()=>{
//          if (method =="POST"){
//             const response =await axios.post(API_LINK , data=Data)
//             console.log(response)
//             if ( response.status==200){
                
//                 setRes(response.data)
//             }
//             else console.log("error" , response.statusText)
//          }
//          else{

//             const response =await axios.get(API_LINK)
//             if ( response.status==200){
//                 setRes(response.data)
//                 console.log(res)
//             }
//             else console.log("error" , response.statusText)

//          }
//       }


//     }, [Data])
//     return res
// }

const useCallAPI=1
export default useCallAPI
