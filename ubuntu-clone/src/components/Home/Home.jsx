import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux'
import { RxCross2 } from "react-icons/rx";
import { FaRegSquare } from "react-icons/fa6";
import { FaMinus } from "react-icons/fa6";
import { closeapp } from '../../store/softwareSlice';
import { useAutoAnimate } from '@formkit/auto-animate/react';
import { minimizeapp } from '../../store/softwareSlice';
import Draggable from 'react-draggable';


function Home() {
  const apps = useSelector(state => state.softwares)
  const OpenedApps = apps.softwares.filter(app => app.isOpen == true)
  const dispatch = useDispatch()
  const [maximizeApp, setMaximizeApp] = useState({})
  const [parentAnimate] = useAutoAnimate()
  const maximizeWindow = (appName) => {
    setMaximizeApp((prevState) => ({
      [appName]: !prevState[appName]
    }))
  }


  return (
    <div className='w-full' ref={parentAnimate}>
      {OpenedApps.map((app) => (
        <Draggable>
          <div>
            <div style={{ zIndex: String(app.zindx) }} key={app.name} class={`window  ${maximizeApp[app.name] ? 'top-0 left-0 w-[100%] h-screen' : 'top-20 left-96 w-1/2 h-auto'}  ${app.display} absolute flex flex-col items-center bg-white border border-gray-200 rounded-lg shadow    dark:border-gray-700 dark:bg-gray-900`}>
              <div class="leading-normal">
                <div className='flex  h-10 justify-end items-center text-white gap-5 relative top-0 bg-zinc-800 pr-4'>
                  <FaMinus onClick={() => dispatch(minimizeapp(app))} />
                  <FaRegSquare onClick={() => (maximizeWindow(app.name))} />
                  <RxCross2 className='text-white text-xl bg-orange-700 rounded-full border-orange-700 border-2' onClick={() => dispatch(closeapp(app))} />
                </div>
                <div className='p-5'>
                  <h5 class="mb text-2xl font-bold tracking-tight text-gray-900 dark:text-white text-center">{app.name}</h5>
                  <p class="mb-3 pt-2 h-80 font-normal text-gray-700 dark:text-gray-400">This is the {app.name} workspace, currently in an open state. If you would like to close it, simply click the "X" button located in the title bar above. This button will allow you to exit the Calendar view and return to your previous screen..</p>
                </div>
              </div>
            </div>
          </div>
        </Draggable>
      ))}
    </div>
  )
}


export default Home