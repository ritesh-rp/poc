import { useNavigate } from 'react-router-dom';
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import Login from "../Login";
import { Navigate } from "react-router-dom";
import ListApps from "../ListApps";
import { useState } from 'react';
import { useAutoAnimate } from '@formkit/auto-animate/react';
import { openapp } from '../../store/softwareSlice';

function Footer() {
    const authUser = sessionStorage.getItem("userData")
    const [toggleAllApps, setToggleAllApps] = useState(true)
    const [parentAnimate] = useAutoAnimate()
    const apps = useSelector(state=> state.softwares)
    const filteredAppList = apps.softwares.filter(app => app.isOpen==true)
    console.log("filteredAppList",filteredAppList)
    const navigate = useNavigate()
    const taskbarApps = apps.softwares.filter(app => app.isFavourite == true || app.isOpen == true)
    const dispatch =useDispatch()
  



    return authUser ?
        <footer className=" w-full h-14 shadow bg-opacity-45 bg-black fixed bottom-0 flex items-center justify-between">
            <div ref={parentAnimate} className="flex items-center justify-between gap-5 px-2">

                {taskbarApps.map((app)=>(
                <div className="p-1  rounded-md hover:bg-zinc-700" onClick={()=>{dispatch(openapp(app))}}>
                    <img src={app.icon} className="h-11" alt="na" />
                </div>
                ))}

            </div>
            <div>
                <div ref={parentAnimate} className="p-2 rounded-md hover:bg-zinc-700 mx-2" onClick={() => {
                    navigate(toggleAllApps ? '/listapps' : '/');
                    setToggleAllApps(!toggleAllApps);
                }}>
                    <img src="https://i.postimg.cc/7LsMvj2H/GO5ql-Aw-Xne1z8-Fm-T0vr-L-transformed.png" className="h-7" alt="na" />
                </div>
            </div>
        </footer>
        :
        null
}

export default Footer;