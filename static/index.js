const signUpBtn = document.getElementById('sign-up')
const logOutBtn = document.getElementById('log-out')

function confirm_delete() {
    return confirm('Are you sure you want to delete?')
}

signUpBtn.addEventListener('click', () => {
  window.location.href = '/sign_up'
})

logOutBtn.addEventListener('click', () => {
  window.location.href = '/log_out'
})
