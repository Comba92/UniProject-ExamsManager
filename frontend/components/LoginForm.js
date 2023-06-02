import axios from 'axios'
import { client } from '../config.js'
import { useRouter } from 'next/router'
import { useState } from 'react'

export default function LoginForm({ login }) {
  const router = useRouter()
  const [errorMessage, setError] = useState(null)
  
  async function handleLogin(event) {
    event.preventDefault()
    setError(null)

    const formData = new FormData(event.target)
    try {
      const req = await client.post(`/login`, {
        username: formData.get("username"),
        type: formData.get("type")
      })
      // login returns just one result 
      const user = await req.data
      user.type = formData.get("type")
      
      login(user)
      window.localStorage.setItem("loggedUser", JSON.stringify(user))
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <div>
      <p>Benvenuti alla pagina di gestione degli esami.</p>
      <form onSubmit={handleLogin}>
        <fieldset>
          <legend>
            <input type='radio' name='type' value='STUDENT' defaultChecked/>
            <label>Studenti</label>
            <input type='radio' name='type' value='TEACHER'/>
            <label>Docenti</label>
          </legend>
        <input type="number" name="username"/>
        <input type="text" name="password" />
        <button type="submit">Log In</button>
        </fieldset>
      </form>
      <div>{errorMessage}</div>
    </div>
  )
}