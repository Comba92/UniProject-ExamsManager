import ViewButton from "./ViewButton";
import { useState, useEffect } from "react"
import { API_URL } from "../config";
import axios from "axios";

export default function StudentsArea({ user, logout }) {
  const [currentView, setView] = useState(null)
  const views = [
    {
      title: "Iscrizione Corsi",
      route: `${API_URL}/students/${user.idStudent}/courses`,
      actions: [
        {
          title: 'discriviti',
          execute: async (entry) => {
            try {
              await axios.post(`${API_URL}/students/${user.idStudent}/unsubscribe`, {
                idCourse: entry.idCourse
              })
            } catch (e) { console.log(e) }
          }}
      ]
    },
    {
      title: 'Visualizza Esiti',
      route: `${API_URL}/students/${user.idStudent}/results`,
      actions: []
    },
    {
      title: 'Visualliza Storico',
      route: `${API_URL}/students/${user.idStudent}/history`,
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