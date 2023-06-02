import { useEffect } from "react";
import EntryView from "./EntryView"

export default function ResultsView({ list, view, setView }) {  
  return (
    <div>
      <h1>{view.title}</h1>
        <ol>
          { list.map(e => (
            <div>
              <EntryView entry={e} />
              { view.actions.map(a => 
                <button onClick={async () => { await a.execute(e); await setView() }}>
                  {a.title}
                </button>)
              }
            </div>
          ))}
        </ol>
    </div>
  )
}