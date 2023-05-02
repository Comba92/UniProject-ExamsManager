import { useState, useEffect } from 'react'

import Navbar from '../components/Navbar'
import LoginForm from '../components/LoginForm'
import StudentsArea from '../components/StudentsArea'
import TeacherArea from '../components/TeachersArea'

export default function Home() {
  const [user, setUser] = useState(null)
 
  useEffect(() => {
    setUser(JSON.parse(window.localStorage.getItem("loggedUser")))
  }, [])

  function renderSwitch(u) {
    switch(u.type) {
      case 'STUDENT': return <StudentsArea user={u} logout={() => setUser(null)} />
      case 'TEACHER': return <TeacherArea user={u} logout={() => setUser(null)} />
    }
  }

  return (
    <div>
      <Navbar />
      { user === null 
        ? <LoginForm login={setUser}/> 
        : renderSwitch(user)
      }
    </div>
  )
}