import axios from 'axios'
import { API_URL } from '../config.js'
import { useRouter } from 'next/router'

export default function LoginForm({ login, error }) {
  const router = useRouter()
  
  async function handleLogin(event) {
    event.preventDefault()
    const formData = new FormData(event.target)
    try {
      const req = await axios.get(`${API_URL}/studenti`)
      const users = req.data.results
      const user = users.find(u => u.idStudente == formData.get("matricola"))
      if (user) {
        login(user)
        router.push('/students/')
      }
    } catch (e) { 
      console.log(e.message)
      error(e.message)
    }
  }
    
  return (
    <div>
      <p>Benvenuti alla pagina di gestione degli esami.</p>
      <form onSubmit={handleLogin}>
        <input type="number" name="matricola" />
        <button type="submit">Log In</button>
      </form>
    </div>
  )
}