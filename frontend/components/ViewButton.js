import axios from 'axios'
import { useState } from 'react'
import ResultsView from './ResultsView'

export default function ViewButton({ title, API_path, actions, setView }) {
  async function getView() {
    try {
      const req = await axios.get(API_path)
      const res = req.data.results
      setView(<ResultsView list={res} title={title} actions={actions}/>)
    } catch(e) { 
      setView(<p>Something went wrong...</p>) 
    }
  }

  return (
    <button onClick={getView}>{title}</button>
  )
}