import { useDispatch } from 'react-redux';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/react'
import ToggleButton from '../utilities/ToggleButton';
import authService from '../../appwrite/auth';
import {login,logout} from '../../store/authSlice'
// icons

import { IoLockClosedSharp } from "react-icons/io5";
import { MdOutlineSettings } from "react-icons/md";
import { HiSpeakerWave } from "react-icons/hi2";
import { IoIosPower } from "react-icons/io";
import { PiNetworkFill } from "react-icons/pi";
import { MdBrightnessMedium } from "react-icons/md";
import { GoTriangleDown } from "react-icons/go";
import { MdOutlineAccessibilityNew } from "react-icons/md";
import { LuNetwork } from "react-icons/lu";
import { GoTriangleRight } from "react-icons/go";
import { useNavigate } from 'react-router-dom';

export default function PowerDropDown() {
    const dispatch = useDispatch();
    const navigate = useNavigate()
    function toggleAccordion(index) {
        document.getElementById(`accordion-content-${index}`).classList.toggle("hidden");
        document.getElementById(`arrow-icon-${index}`).classList.toggle("rotate-90");
    }

    const accessItems = ["High contrast", "Zoom", "Large Text", "Screen reader", "Screen Keyboard", "Visual Alert", "Sticky Keys", "Slow Keys", "Bounce Keys", "Mouse Keys"]
    return (

        <>


                    {/*  #########################  Accessibility ###########################      */}

            <Menu as="div" className="relative inline-block text-left">
                <div>
                    <MenuButton className="text-white flex items-center">
                        <MdOutlineAccessibilityNew />&nbsp;
                        <GoTriangleDown />
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    </MenuButton>
                </div>

                <MenuItems
                    transition
                    className="absolute left-1/2 transform -translate-x-1/2 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 transition focus:outline-none data-[closed]:scale-95 data-[closed]:transform data-[closed]:opacity-0 data-[enter]:duration-100 data-[leave]:duration-75 data-[enter]:ease-out data-[leave]:ease-in "
                >
                    <div className="py-4">
                        {accessItems.map((item,index) => (
                            <MenuItem className="hover:bg-zinc-200 cursor-default" key={index}>
                                <div className='grid grid-cols-4 px-4 p-1 '>
                                    <div className='col-span-3 text-gray-700'>{item}</div>
                                    <div className='col-span-1'><ToggleButton /></div>
                                </div>
                            </MenuItem>
                        ))}
                    </div>
                </MenuItems>
            </Menu>





            {/*  #########################  power ###########################      */}



            <Menu as="div" className="relative inline-block text-left">
                <div>
                    <MenuButton className="text-white flex items-center gap-2">
                        <MdBrightnessMedium />
                        <PiNetworkFill />
                        <HiSpeakerWave />
                        <IoIosPower />
                        <GoTriangleDown />
                    </MenuButton>
                </div>
                <MenuItems
                    transition
                    className="absolute right-0 z-10 mt-2 w-80 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 transition focus:outline-none data-[closed]:scale-95 data-[closed]:transform data-[closed]:opacity-0 data-[enter]:duration-100 data-[leave]:duration-75 data-[enter]:ease-out data-[leave]:ease-in"
                >
                    <div className="py-4">

                        <MenuItem onClick={(e) => { e.preventDefault() }} >
                            <div className='grid grid-cols-12 px-7 py-2 items-center hover:bg-zinc-200 text-gray-700'>
                                <div className='col-span-2 '><HiSpeakerWave /></div>
                                <div className='col-span-10'>
                                    <input type="range" min={0} max="100" className="range w-full" />
                                </div>
                            </div>
                        </MenuItem>

                        <div className='flex justify-center'><hr className='w-40 my-2' /></div>


                        <div onClick={() => { toggleAccordion(1) }}>
                            <div className='grid grid-cols-12 cursor-default px-7 py-2 items-center cursor-default hover:bg-zinc-200 text-gray-700'>
                                <div className='col-span-1 '><PiNetworkFill /></div>
                                <div className='col-span-10 pl-2'>Wired Connected</div>
                                <div className='col-span-1' id="arrow-icon-1"><GoTriangleRight /></div>
                            </div>
                        </div>
                        <div className="hidden" id="accordion-content-1">
                            <div className='flex justify-center'><hr className='w-full' /></div>
                            <MenuItem onClick={(e) => { e.preventDefault() }} >
                                <div className='grid grid-cols-12 cursor-default px-7 py-2 items-center hover:bg-zinc-200 text-gray-700'>
                                    <div className='col-span-1 '></div>
                                    <div className='col-span-10 pl-2'>Turn Off</div>
                                </div>
                            </MenuItem>
                            <MenuItem onClick={(e) => { e.preventDefault() }} >
                                <div className='grid grid-cols-12 cursor-default px-7 py-2 items-center hover:bg-zinc-200 text-gray-700'>
                                    <div className='col-span-1 '></div>
                                    <div className='col-span-10 pl-2'>Wired Setting</div>
                                </div>
                            </MenuItem>
                            <div className='flex justify-center'><hr className='w-full' /></div>
                        </div>




                        <div onClick={() => { toggleAccordion(2) }}>
                            <div className='grid grid-cols-12 cursor-default px-7 py-2 items-center hover:bg-zinc-200 text-gray-700'>
                                <div className='col-span-1 '><MdBrightnessMedium /></div>
                                <div className='col-span-10 pl-2'>Night Light On</div>
                                <div className='col-span-1' id="arrow-icon-2"><GoTriangleRight /></div>
                            </div>
                        </div>
                        <div className="hidden" id="accordion-content-2">
                            <div className='flex justify-center'><hr className='w-full' /></div>
                            <MenuItem onClick={(e) => { e.preventDefault() }} >
                                <div className='grid grid-cols-12 cursor-default px-7 py-2 items-center hover:bg-zinc-200 text-gray-700'>
                                    <div className='col-span-1 '></div>
                                    <div className='col-span-10 pl-2'>Disable Until Tomorrow</div>
                                </div>
                            </MenuItem>
                            <MenuItem onClick={(e) => { e.preventDefault() }} >
                                <div className='grid grid-cols-12 cursor-default px-7 py-2 items-center hover:bg-zinc-200 text-gray-700'>
                                    <div className='col-span-1 '></div>
                                    <div className='col-span-10 pl-2'>Turn Off</div>
                                </div>
                            </MenuItem>
                            <MenuItem onClick={(e) => { e.preventDefault() }} >
                                <div className='grid grid-cols-12 cursor-default px-7 py-2 items-center hover:bg-zinc-200 text-gray-700'>
                                    <div className='col-span-1 '></div>
                                    <div className='col-span-10 pl-2'>Display Settings</div>
                                </div>
                            </MenuItem>
                            <div className='flex justify-center'><hr className='w-full' /></div>
                        </div>


                        <div className='flex justify-center'><hr className='w-40 my-2' /></div>

                        <MenuItem onClick={(e) => { e.preventDefault() }} >
                            <div className='grid grid-cols-12 cursor-default px-7 py-2 items-center hover:bg-zinc-200 text-gray-700'>
                                <div className='col-span-1 '><MdOutlineSettings /></div>
                                <div className='col-span-10 pl-2'>Setting</div>
                            </div>
                        </MenuItem>
                        <MenuItem onClick={(e) => { e.preventDefault() }} >
                            <div className='grid grid-cols-12 cursor-default px-7 py-2 items-center hover:bg-zinc-200 text-gray-700'>
                                <div className='col-span-1 '><IoLockClosedSharp /></div>
                                <div className='col-span-10 pl-2'>Lock</div>
                            </div>
                        </MenuItem>




                        <div onClick={() => { toggleAccordion(3) }}>
                            <div className='grid grid-cols-12 cursor-default px-7 py-2 items-center hover:bg-zinc-200 text-gray-700'>
                                <div className='col-span-1 '><IoIosPower /></div>
                                <div className='col-span-10 pl-2'>Power Off / Log Out</div>
                                <div className='col-span-1' id="arrow-icon-3"><GoTriangleRight /></div>
                            </div>
                        </div>
                        <div className="hidden" id="accordion-content-3">
                            <div className='flex justify-center'><hr className='w-full' /></div>
                            <MenuItem onClick={(e) => { authService.logOut();dispatch(logout());}} >
                                <div className='grid grid-cols-12 cursor-default px-7 py-2 items-center hover:bg-zinc-200 text-gray-700'>
                                    <div className='col-span-1 '></div>
                                    <div className='col-span-10 pl-2'>Log Out</div>
                                </div>
                            </MenuItem>
                            <MenuItem onClick={(e) => { e.preventDefault() }} >
                                <div className='grid grid-cols-12 cursor-default px-7 py-2 items-center hover:bg-zinc-200 text-gray-700'>
                                    <div className='col-span-1 '></div>
                                    <div className='col-span-10 pl-2'>Suspend</div>
                                </div>
                            </MenuItem>
                            <MenuItem onClick={(e) => { console.log("rITESHHHHHHHHHHHHHHH");}} >
                                <div className='grid grid-cols-12 cursor-default px-7 py-2 items-center hover:bg-zinc-200 text-gray-700'>
                                    <div className='col-span-1 '></div>
                                    <div className='col-span-10 pl-2'>Power Off...</div>
                                </div>
                            </MenuItem>
                            <div className='flex justify-center'><hr className='w-full' /></div>
                        </div>





                        
                    </div >

                </MenuItems>
            </Menu >
        </>
    )
}
