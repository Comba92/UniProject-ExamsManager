import EntryView from "./EntryView"
import { useState } from 'react'

export default function ResultsView({ list, view }) {
  return (
    <div>
      <h1>{view.title}</h1>
        <ol>
          { list.map(e => (
            <div>
              <EntryView entry={e} />
              { view.actions.map(a => 
                <button onClick={async () => { await a.execute(e); }}>
                  {a.title}
                </button>)
              }
            </div>
          ))}
        </ol>
    </div>
  )
}