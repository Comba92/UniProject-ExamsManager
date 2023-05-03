import axios from 'axios'
import { useState } from 'react'
import ResultsView from './ResultsView'
import ErrorMessage from './ErrorMessage'

export default function ViewButton({ view, setView }) {
  async function getView() {
    try {
      const req = await axios.get(view.route)
      const res = req.data.query
      if(res.length == 0) throw new Error('Nessun risultato!')
      setView(<ResultsView list={res} view={view}/>)
    } catch(e) { 
      setView(<ErrorMessage error={e.message} />) 
    }
  }

  return (
    <button onClick={getView}>{view.title}</button>
  )
}