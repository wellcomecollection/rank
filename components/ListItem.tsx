const ListItem = ({ children }) => {
  return (
    <li
      style={{
        listStyle: 'none',
        padding: 0,
        margin: '0 0 25px 0',
        borderTop: '5px solid silver',
      }}
    >
      {children}
    </li>
  )
}

export default ListItem
