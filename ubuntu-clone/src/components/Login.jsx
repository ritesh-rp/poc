import { Navigate } from 'react-router-dom'
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { useForm } from "react-hook-form"
import authService from '../appwrite/auth'
import { login as authlogin } from '../store/authSlice'
import { Link } from 'react-router-dom'

// icons
import { AiOutlineEyeInvisible, AiOutlineEye } from "react-icons/ai";
import { Container } from 'postcss'
import { BiLoaderCircle } from "react-icons/bi";





function Login() {
    const navigate = useNavigate()
    const [email, setEmail] = useState('ritesh88822@gmail.com')
    const [loader,setLoader] =useState(false)
    const [password, setPassword] = useState('')
    const [showPass, setShowpass] = useState(false)
    const dispatch = useDispatch()
    const [error, setError] = useState("")
    const [errAnimate, setErrAnimate] = useState(false)
    // const authUser = useSelector(state => state.auth.status)
    const authUser = sessionStorage.getItem("userData")
    

    const login = async (e) => {
        e.preventDefault()
        setLoader(true)
        setError("")
        setErrAnimate(false)
        try {
            const session = await authService.logIn(email, password)
            console.log("object---------,", session)
            if (session) {
                const userData = await authService.getCurrentUser()
                console.log("this is the current user...........", userData);
                if (userData) {
                    dispatch(authlogin(userData))
                    sessionStorage.setItem("userData", JSON.stringify(userData.status))
                    navigate("/")
                }
            }
        } catch (error) {
            setError(error.message)
            setErrAnimate(true)
        }finally{
            setLoader(false)
        }
    }
    return authUser ? navigate('/') :
            <div className="absolute top-0 left-0 w-full -z-10  backdrop-blur-md flex flex-col justify-center items-center" style={{height:'100vh'}}>
                <div className='relative flex items-center justify-center flex-col' >
                    <img className='rounded-full h-28 w-28' src="https://c4.wallpaperflare.com/wallpaper/627/395/613/blue-controller-dualshock-entertainment-wallpaper-preview.jpg" alt="" />
                    <h1 className='text-white text-3xl pt-3'>Ritesh</h1><br />
                </div>
                <form onSubmit={login}>
                    <div className={`relative left-4 flex items-center justify-center ${errAnimate ? 'bounce-animation' : null}`}>
                        <input type={showPass ? 'text' : 'password'} name="password" onKeyUp={(e) => { setPassword(e.target.value) }} id="password" placeholder='Password' className='p-2  m-2  h-10 w-72 rounded  focus:ring-2 focus:ring-orange-700 focus:outline-none border-orange-700' />
                        <span onClick={() => { setShowpass(!showPass) }} className='flex'>
                            {showPass ? <AiOutlineEyeInvisible className='relative  right-9 text-xl font-bold' /> : <AiOutlineEye className='relative  right-9 font-bold text-xl' />}
                            <div className={`relative ${loader ? 'block' : 'hidden'} animate-spin font-bold text-2xl text-gray-300`}>

                            <BiLoaderCircle  /> 
                            </div>
                        <button type="submit" hidden={true} />
                        </span >
                    </div>
                </form>
                {error && <div className="text-white mt-4">{error}</div>}
            </div >
}
export default Login;