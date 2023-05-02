import ViewButton from "./ViewButton";
import { useState } from "react"
import { API_URL } from "../config";

export default function StudentsArea({ user, logout }) {
  const [currentView, setView] = useState(null)
  const views = []

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