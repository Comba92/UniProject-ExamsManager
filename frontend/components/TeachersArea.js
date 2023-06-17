import ViewButton from "./ViewButton";
import { useState, useEffect } from "react"
import {client} from '../config'


export default function TeachersArea({ user, logout }) {
  const [currentView, setView] = useState(null)
  
  const createCourse = async (formData) => {
    await client.post(`/teachers/${user.idTeacher}/createCourse/`, {
      title: formData.get("title")
    })
  }

  const createExam = async (idCourse, date) => {
    await client.post(`/teachers/${user.idTeacher}/createExam/`, {
      idCourse, date
    })
  }
  
  const views = [
    {
      title: 'Crea Corso',
      input: {
        form: ['title'],
        submit: createCourse
      },
      actions: []
    },
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
    {
      title: 'Assegna Voti',
      route: `teachers/${user.idTeacher}/sittings`,
      actions: [
        {
          title: 'assegna voto',
          type: 'number',
          execute: async (mark, entry) => {
            try {
              await client.post(`/teachers/${user.idTeacher}/assignMark`, {
                mark: mark, idSitting: entry.idSitting
              })
            } catch (e) { console.log(e) }
          }
        }
      ]
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