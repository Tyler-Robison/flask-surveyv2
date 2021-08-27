const thanksButtons = document.querySelectorAll('.thanks-button')

const thanksArray = Array.from(thanksButtons)

for (let i = 0; i < thanksArray.length; i++) {
    thanksArray[i].formAction = `/change/${i}`
}