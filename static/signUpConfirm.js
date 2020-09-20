const submitBtn = document.getElementById('sign-up-submit')
const userInputs = document.querySelectorAll('input')
const signUpForm = document.querySelector('form')
const textNode = document.createElement('p')
const fieldMessage = textNode.innerText = 'All fields are required.'

const submitBtnHandler = () => {
  if (!userInputs.value) {
    signUpForm.appendChild(fieldMessage)
    window.location.href = '/sign_up'
  } else {
    console.log('Made it into else')
    alert('Thank you for signing up!')
    window.location.href = '/'
  }
}

submitBtn.addEventListener('click', submitBtnHandler)
