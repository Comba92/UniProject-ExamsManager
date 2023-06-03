import { useEffect } from "react";
import EntryView from "./EntryView"
import UserInputForm from "./UserInputForm";

export default function ResultsView({ list, view, setView }) {  
  useEffect(() => console.log(view), [])

  return (
    <div>
      <h1>{view.title}</h1>
      {view.input ? <UserInputForm APICall={view.input}/> : null}
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