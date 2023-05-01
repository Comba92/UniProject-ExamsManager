import Navbar from "../../components/Navbar";
import ViewButton from "../../components/ViewButton";
import { useState, useEffect } from "react"
import { API_URL } from "../../config";
import Link from 'next/link'

const API_paths = [
  `${API_URL}/studenti/1/esiti`,
  `${API_URL}/studenti/1/storico`,
]

export default function PersonalArea() {
  const [currentView, setView] = useState(null)

  useEffect(() => console.log(currentView))

  return (
    <div>
      <Navbar />
      <h1>Benvenuto nell'area personale!</h1>
      <div><Link href="/">Iscrizione Corsi</Link></div>
      <div><Link href="/">Iscrizione Appelli</Link></div>
      <ViewButton 
        title="Visualizza Esiti"
        API_path={API_paths[0]}
        actions={[]} setView={setView}
      />
      <ViewButton
        title="Visualliza Storico" 
        API_path={API_paths[1]}
        actions={[]} setView={setView}
      />
      {currentView}
    </div>
  )
}