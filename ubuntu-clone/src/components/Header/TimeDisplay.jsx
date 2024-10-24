import React, { useEffect } from 'react'
import { useState } from 'react'


function TimeDisplay() {
  const [time, setTime] = useState('')
  const [date, setDate] = useState('')

  const currentTime = () => {
    const currenttime = new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })
    const currentdate = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    setTime(currenttime)
    setDate(currentdate)
  }

  useEffect(() => {
    currentTime()
    setInterval(() => {
      currentTime()
    }, 30000);
    return () => {
      clearInterval()
    }
  }, [])

  return (
    <div>{date}&nbsp;&nbsp;&nbsp;{time}</div>
  )
}
export default TimeDisplay