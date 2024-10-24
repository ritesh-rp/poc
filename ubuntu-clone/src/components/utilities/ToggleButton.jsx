import React,{useState} from 'react'

function ToggleButton() {
    const [isChecked, setIsChecked] = useState(false)

    const handleCheckboxChange = () => {
        setIsChecked(!isChecked)
    }

    return (
        <>
            <label className='flex cursor-pointer select-none items-center'>
                <div className='relative'>
                    <input
                        type='checkbox'
                        checked={isChecked}
                        onChange={handleCheckboxChange}
                        className='sr-only'
                    />
                    <div
                        className={`box block border-2 border-gray-300 h-6 w-12 rounded-full ${isChecked ? 'bg-purple-700' : 'bg-zinc-300'
                            }`}
                    ></div>
                    <div
                        className={`absolute border-2 border-gray-300 left-0 top-0 flex h-6 w-6 items-center justify-center rounded-full bg-white transition ${isChecked ? 'translate-x-full' : ''
                            }`}
                    ></div>
                </div>
            </label>
        </>
    )
}

export default ToggleButton