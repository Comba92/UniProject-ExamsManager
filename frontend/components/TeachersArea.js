import ViewButton from "./ViewButton";
import { useState, useEffect } from "react"
import {client} from '../config'


export default function StudentsArea({ user, logout }) {
  const [currentView, setView] = useState(null)
  const views = [
    {
      title: 'Visualizza Corsi',
      route: `/teachers/${user.idTeacher}/courses`,
      actions: []
    },
    {
      title: 'Visualliza Appelli',
      route: `/teachers/${user.idTeacher}/exams`,
      actions: []
    },
  ]

function resetSession() {
    window.localStorage.removeItem("loggedUser")
    logout()
  }

  return (
    <div>
      <h1>Benvenuto nell'area personale, {user.name}!</h1>
      <p><button onClick={resetSession}>Logout</button></p>
      {
        views.map(v => 
          <ViewButton 
            view={v} setView={setView}
          />
        )
      }
      {currentView}
    </div>
  )
}