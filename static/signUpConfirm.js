const submitBtn = document.getElementById('sign-up-submit')

const submitBtnHandler = () => {
  window.location.href = '/'
  alert('Thank you for signing up!')
}

submitBtn.addEventListener('click', submitBtnHandler)
