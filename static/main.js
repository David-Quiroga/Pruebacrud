const userFrom = document.querySelector('#userForm')
//Variable vacia
let users = []

window.addEventListener('DOMContentLoaded', async () => {
  const response = await fetch("/api/users");
  const data = await response.json()
  users = data
  renderUser(users)
});
// Tiene codigo asincrono
userFrom.addEventListener('submit', async e => {
  e.preventDefault()

  const company = userFrom['company'].value
  const email   = userFrom['email'].value
  const descrip = userFrom['descrip'].value
  const sector  = userFrom['sector'].value

  const response = await fetch('/api/users', {
    method: 'POST',
// Los datos que se envian del server es un json
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      company:  company,
      email:    email,
      descrip:  descrip,
      sector:   sector
    })
  })
  //metodos asincronos
  const data = await response.json()
  console.log(data)
})

function  renderUser(users) {
  const userList = document.querySelector('#userList')
  userList.innerHTML = ''
  users.forEach((user) => {
    const userItem = document.createElement('li')
    userItem.classList = "list-group-item list-group-item-dark my-2"
    userItem.innerHTML = `
    <header class="d-flex justify-content-between align-items-center">
    <h3>${user.company}</h3>
    </header>
    <p>${user.email}</p>
    <p>${user.sector}</p>
    <p class="text-truncate">${user.descrip}</p>
    `
    userList.append(userItem)
  })

  //Se crean los usuarios con el foreach

}