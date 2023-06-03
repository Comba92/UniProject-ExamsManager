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

  const createExam = async (formData) => {
    await client.post(`/teachers/${user.idTeacher}/createExam/`, {
      idCourse: formData.get("idCourse")
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
      title: 'Crea Appello',
      input: {
        form: ['idCourse'],
        submit: createExam
      },
      actions: []
    },
    {
      title: 'Visualliza Appelli',
      route: `/teachers/${user.idTeacher}/exams`,
      actions: []
    },
    {
      title: 'Assegna Voti',
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