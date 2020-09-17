const logOutBtn = document.getElementById('log-out')

logOutBtn.addEventListener('click', () => {
  console.log('Log out button clicked')
  window.location.href = '/log_out'
})
