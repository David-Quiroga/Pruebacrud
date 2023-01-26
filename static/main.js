const userForm = document.querySelector("#userForm");

let users = []

window.addEventListener("DOMContentLoaded", async () => {
  const response = await fetch("/api/users");
  const data = await response.json()
  users = data
  renderUser(users)
});

userForm.addEventListener('submit', async e => {
  e.preventDefault()
  const company   = userForm['company'].value
  const email     = userForm['email'].value
  const descrip   = userForm['descrip'].value
  const sector    = userForm['sector'].value
  const response =  await fetch('/api/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      company,
      email,
      descrip,
      sector
    })
  })

  const data = await response.json()
  
  users.unshift(data)
  
  renderUser(users)
  
  userForm.reset();
})

function renderUser(users) {
  const userList = document.querySelector('#userList')
  userList.innerHTML = ''

  users.forEach(user => {
    const userItem = document.createElement('li')
    userItem.classList = 'list-group-item list-group-item-warning my-2'
    userItem.innerHTML =  `
      <header>
        <h3>${user.company}</h3>
      </header>
      <p>${user.email}</p>
      <p>${user.descrip}</p>
      <p>${user.sector}</p>
    `
    userList.append(userItem)
  })

}