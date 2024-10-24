import { useNavigate } from 'react-router-dom';
import React, { useState, useEffect,useMemo } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { FiSearch } from "react-icons/fi";
import { useAutoAnimate } from '@formkit/auto-animate/react'
import { motion } from 'framer-motion';
import { randomizer } from '../store/softwareSlice';
import { useLocation } from 'react-router-dom';
import {openapp} from '../store/softwareSlice';



function ListApps() {
    const [animationParent] = useAutoAnimate()
    const [search,setSearch] = useState()
    let apps = useSelector((state) => state.softwares)
    apps = useMemo(() => search?apps.softwares.filter(APP => APP.name.toLowerCase().startsWith(search.toLowerCase()), [search]):apps)
    const dispatch = useDispatch()
    const [showapp, setShowapp] = useState(false)
    const navigate = useNavigate()



    const appList = apps.softwares.map(app => {
        return (
            <div className='w-full flex flex-col items-center justify-center  rounded-lg p-3 m-2 ' key={app.name} onClick={()=>{dispatch(openapp(app));navigate('/')}}>
                <img className="h-[4.2rem]" src={app.icon} alt={app.name} />
                <h3 className='text-white py-1'>{(app.name).length > 8 ? (app.name).slice(0, 7) + "..." : app.name}</h3>
            </div>
        )
    })

    setTimeout(() => {
        setShowapp(true)
    }, 10);

    function randomize() {
        dispatch(randomizer())
    }
    return (
        <>
            <div className=' absolute top-0 right-0 bg-black bg-opacity-50 h-[100vh] w-full -z-10'>
                <div className='h-[80vh] grid grid-rows-10 grid-cols-1 gap-3 mx-[25em] my-10 pt-10' >
                    <div className='row-span-1 flex justify-center'>
                        <FiSearch className='h-10 text-gray-400 text-xl relative left-9' />
                        <input type="search" onKeyUp={(e)=>{console.log("sddddddddddddddddddddddd");setSearch(e.target.value)}} placeholder='Type to search' className='h-10 w-96 pl-12 rounded-full focus:ring-2 focus:ring-orange-700 focus:outline-none border-orange-700' />
                    </div>
                    <div className='allApps relative overflow-scroll mt-[1.5rem] row-span-2 row-span-8 h-[58vh]'>
                        <div className='grid grid-cols-6 ' ref={animationParent} >{showapp && appList}</div>
                    </div>
                    <div className='row-span-2 flex justify-evenly px-52 mt-8 text-white text-xl'>
                        <div className='min-w-48 min-h-10 text-center hover:border-b-4 border-r-orange-600'>Frequent</div>
                        <div className='min-w-48 min-h-10 text-center hover:border-b-4 border-r-orange-600' onClick={randomize}>All</div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default ListApps