import axios from 'axios'
import { useState } from 'react'
import ResultsView from './ResultsView'
import ErrorMessage from './ErrorMessage'

export default function ViewButton({ title, APIRoute, actions, setView }) {
  async function getView() {
    try {
      const req = await axios.get(APIRoute)
      const res = req.data.results
      setView(<ResultsView list={res} title={title} actions={actions}/>)
    } catch(e) { 
      setView(<ErrorMessage error={e.message} />) 
    }
  }

  return (
    <button onClick={getView}>{title}</button>
  )
}