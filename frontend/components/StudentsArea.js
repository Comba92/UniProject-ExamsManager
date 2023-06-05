import ViewButton from "./ViewButton";
import { useState, useEffect } from "react"
import {client} from '../config'

export default function StudentsArea({ user, logout }) {
  const [currentView, setView] = useState(null)
  const views = [
    {
      title: "Corsi a cui sei iscritto",
      route: `/students/${user.idStudent}/marks`,
      actions: [
        {
          title: 'discriviti',
          type: 'button',
          execute: async (entry) => {
            try {
              await client.post(`/students/${user.idStudent}/unsubscribe`, {
                idCourse: entry.idCourse
              })
            } catch (e) { console.log(e) }
          }
        }
      ]
    },
    {
      title: "Iscrizione Corsi",
      route: `/students/${user.idStudent}/courses`,
      actions: [
        {
          title: 'iscriviti',
          type: 'button',
          execute: async (entry) => {
            try {
              await client.post(`/students/${user.idStudent}/subscribe`, {
                idCourse: entry.idCourse
              })
            } catch (e) { console.log(e) }
          }}
      ]
    },
        {
      title: "Appelli a cui sei iscritto",
      route: `/students/${user.idStudent}/reserved`,
      actions: [
        {
          title: 'discriviti',
          type: 'button',
          execute: async (entry) => {
            try {
              await client.post(`/students/${user.idStudent}/unreserve`, {
                idExam: entry.idExam
              })
            } catch (e) { console.log(e) }
          }}
      ]
    },
    {
      title: "Iscrizione Appelli",
      route: `/students/${user.idStudent}/exams`,
      actions: [
        {
          title: 'iscriviti',
          type: 'button',
          execute: async (entry) => {
            try {
              await client.post(`/students/${user.idStudent}/reserve`, {
                idExam: entry.idExam
              })
            } catch (e) { console.log(e) }
          }}
      ]
    },
    {
      title: 'Visualizza Esiti',
      route: `/students/${user.idStudent}/valids`,
      actions: []
    },
    {
      title: 'Visualliza Storico',
      route: `/students/${user.idStudent}/history`,
      actions: []
    },
    {
      title: 'Conferma Voti Finali',
      route: `/students/${user.idStudent}/toValidate`,
      actions: [
         {
          title: 'accetta',
          type: 'button',
          execute: async (entry) => {
            try {
              await client.post(`/students/${user.idStudent}/validate`, {
                finalMark: entry.finalMark
              })
            } catch (e) { console.log(e) }
          }}
      ]
    }
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