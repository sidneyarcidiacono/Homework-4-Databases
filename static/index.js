const signUpBtn = document.getElementById('sign-up')

function confirm_delete() {
    return confirm('Are you sure you want to delete?')
}

signUpBtn.addEventListener('click', () => {
  window.location.href = '/sign_up'
})
