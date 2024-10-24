// import { useNavigate } from 'react-router-dom'
import React from 'react'
import './App.css'
import { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import authService from './appwrite/auth'
import { login, logout } from './store/authSlice'
// import { Provider } from 'react-redux'
import { Header, Footer } from './components'
import { BrowserRouter, Outlet } from 'react-router-dom'
import MainRoutes from './components/Routes/MainRoutes'
import Login from './components/Login'
import { useAutoAnimate } from '@formkit/auto-animate/react'




function App() {
  const [loading, setLoading] = useState(true)
  const authStatus = useSelector((state) => state.auth.status)
  const dispatch = useDispatch()
  const [animationParent] = useAutoAnimate()

  // const [parent, enableAnimations] = useAutoAnimate(/* optional config */)


  // useEffect(() => {
  //   authService.getCurrentUser()
  //     .then((userData) => {
  //       if (userData) {
  //         dispatch(login({ userData }))
  //       }
  //       else {
  //         dispatch(logout())
  //       }
  //     })
  //     .finally(() => setLoading(false))
  // }, [])


  return (
    <div ref={animationParent}>
        <BrowserRouter>
        <Header />
        <MainRoutes />
        <Outlet />
        <Footer />
        </BrowserRouter>
      </div>
  );

}

export default App
