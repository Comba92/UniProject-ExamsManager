import EntryView from "./EntryView"

export default function DataView({ title, list, actions }) {
  return (
    <div>
      <h1>{title}</h1>
      {list.length == 0
       ? <p>Nessun risultato!</p>
       : (
        <ol>
          { list.map(e => <EntryView entry={e} />)}
        </ol>
       )}
    </div>
  )
}