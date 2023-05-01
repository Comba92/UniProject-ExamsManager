export default function EntryView({ entry }) {
  return (
    <li>
    {
      <ul>
        {Object.keys(entry).map(k => `${k}: ${entry[k]}, `)}
      </ul>
    }
    </li>
  )
} 