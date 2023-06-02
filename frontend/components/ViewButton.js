import {client} from '../config'
import { useState } from 'react'
import ResultsView from './ResultsView'
import ErrorMessage from './ErrorMessage'

export default function ViewButton({ view, setView }) {
  async function getView() {
    try {
      const req = await client.get(view.route)
      const res = req.data
      if(res.length == 0) throw new Error('Nessun risultato!')
      setView(<ResultsView list={res} view={view} setView={getView}/>)
    } catch(e) {
      setView(<ErrorMessage error={e.message} />) 
    }
  }

  return (
    <button onClick={getView}>{view.title}</button>
  )
}