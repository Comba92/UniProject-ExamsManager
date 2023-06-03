import axios from 'axios'
import { client } from '../config.js'
import { useRouter } from 'next/router'
import { useState } from 'react'

export default function UserInputForm({ APICall }) {
  const router = useRouter()
  const [message, setMessage] = useState(null)
  
  async function handleInput(event) {
    event.preventDefault()
    setMessage(null)

    const formData = new FormData(event.target)
    try {
      await APICall.submit(formData)
      setMessage('Success!')
    } catch (e) {
      setMessage(e.message)
    }
  }

  return (
    <div>
      <form onSubmit={handleInput}>
        <fieldset>
          <legend>
            aa
          </legend>
        {APICall.form.map(e => <div>{e} <input type={e} name={e} /></div>)}
        <button type="submit">Invia</button>
        </fieldset>
      </form>
      <div>{message}</div>
    </div>
  )
}