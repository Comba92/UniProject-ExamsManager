import { useState, useEffect } from 'react'

import Navbar from '../components/Navbar'
import LoginForm from '../components/LoginForm'
import ErrorMessage from '../components/ErrorMessage'
import PersonalArea from './students'

export default function Home() {
  const [user, setUser] = useState(null)
  const [error, setError] = useState(null)
  
  return (
    <div>
      <Navbar />
      { user === null ? <LoginForm login={setUser} error={setError}/> : null}
      { error !== null ? <ErrorMessage error={error} /> : null }
    </div>
  )
}