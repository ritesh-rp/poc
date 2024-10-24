// import { useNavigate } from "react-router-dom";
// import { useState, useEffect } from "react";
// import { useSelector } from "react-redux";

// export default function Protected({ children, authentication }) {
//     const navigate = useNavigate()
//     const [loader, setLoader] = useState(true)
//     const authStatus = useSelector(state => state.auth.status)

//     useEffect(() => {
//         if (authentication && authStatus !== authentication) {
//             navigate("/login")
//         }
//         else if (!authentication && authStatus !== authentication) {
//             navigate("/")
//         }
//         setLoader(false)
//     }, [navigate, authStatus, authentication])
//     return loader? <h2>Loading...</h2> : <>{children}</>
// }