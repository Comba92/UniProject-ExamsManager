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
                a.type === 'button'
                ? (
                  <button onClick={async () => { await a.execute(e); await setView() }}>
                    {a.title}
                  </button>
                ) : (
                  <div>
                    {a.title}
                    <form onSubmit={
                      async (event)  => {
                        event.preventDefault();
                         const formData = new FormData(event.target)
                        await a.execute(Number(formData.get('value')), e);
                        console.log(formData.get('value'))
                        await setView()
                    }}>
                      <input type={a.type} name="value"/>
                      <button type="submit">invia</button>
                    </form>
                  </div>
                ))
              }
            </div>
          ))}
        </ol>
    </div>
  )
}