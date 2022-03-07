//mobile menu
const burgerIcon = document.querySelector('#burger')
const navbarMenu = document.querySelector('#navLinks')
console.log(navbarMenu)
burgerIcon.addEventListener('click', ()=>{
    navbarMenu.classList.toggle('is-active')
})

