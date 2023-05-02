import ViewButton from "./ViewButton";
import { useState, useEffect } from "react"
import { API_URL } from "../config";
import axios from "axios";

export default function StudentsArea({ user, logout }) {
  const [currentView, setView] = useState(null)
  const views = [
    {
      title: "Iscrizione Corsi"
    },
    {
      title: "Iscrizione Appelli"
    },
    {
      title: 'Visualizza Esiti',
      route: `${API_URL}/studenti/${user.idStudente}/esiti`,
      actions: []
    },
    {
      title: 'Visualliza Storico',
      route: `${API_URL}/studenti/${user.idStudente}/storico`,
      actions: []
    },
  ]

  function resetSession() {
    window.localStorage.removeItem("loggedUser")
    logout()
  }

  return (
    <div>
      <h1>Benvenuto nell'area personale, {user.nome}!</h1>
      <p><button onClick={resetSession}>Logout</button></p>
      {
        views.map(v => 
          <ViewButton 
            title={v.title} APIRoute={v.route}
            actions={v.actions} setView={setView}
          />
        )
      }
      {currentView}
    </div>
  )
}