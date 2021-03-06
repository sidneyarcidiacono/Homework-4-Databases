const logOutBtn = document.getElementById('log-out')
const deleteBtn = document.getElementById('delete-user')
const editUserBtn = document.getElementById('edit_user_button')

const deleteUserHandler = () => {
  confirmDel = confirm('Are you sure you want to delete profile? This cannot be undone.')
  if(confirmDel) {
    window.location.href = '/delete_user'
  } else {
    return
  }
}

deleteBtn.addEventListener('click', deleteUserHandler)

logOutBtn.addEventListener('click', () => {
  console.log('Log out button clicked')
  window.location.href = '/log_out'
})

editUserBtn.addEventListener('click', () => {
  console.log('Edit button clicked')
  window.location.href = '/edit_user'
})
