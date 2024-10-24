import React from 'react'
import { BrowserRouter,Routes,Route } from 'react-router-dom'
import Login from '../Login' 
import SignUp from '../SignUp'
import Home from '../Home/Home'
import ListApps from '../ListApps'
import ProtectedRoutes from './ProtectedRoutes'

function MainRoutes() {
  return (
    <Routes>
        <Route path='/login' element={<Login/>}/>
        <Route path='/signup' element={<SignUp/>}/>
        <Route path='/' element={<ProtectedRoutes children={<Home/>}/>}/>
        <Route path='/listapps' element={<ProtectedRoutes children={<ListApps/>}/>}/>
    </Routes>
)
}

export default MainRoutes;