const step_cards = document.querySelectorAll(".step-card")
const submit_btn = document.getElementById("submit_btn")
const next_btn = document.getElementById("next_btn")
const back_btn = document.getElementById("back_btn")

let current_step = 0


// saved_step = localStorage.getItem('current_step')
// // current_step = saved_step
// console.log("Saved Step: " + saved_step + " is loaded")
// console.log("Current Step: " + current_step + " is loaded")

console.log("Lenght: " + step_cards.length)
function update_step() {
    saveCurrentStep()
    step_cards.forEach((step_card, index) => {
        isActive = index === current_step
        step_card.classList.toggle("animate-swoop-out", !isActive)
        step_card.classList.toggle("animate-swoop-in", isActive)
        step_card.classList.toggle("hidden", !isActive)
        // step_card.classList.toggle("flex", isActive)
    })

    if (current_step > 0) {
        back_btn.disabled = false
    } else {
        back_btn.disabled = true
    }
    if (current_step == step_cards.length - 1) {
        submit_btn.classList.remove("hidden");
        next_btn.classList.add("hidden");
    } else {
        next_btn.classList.remove("hidden");
        submit_btn.classList.add("hidden");
    }
    saveCurrentStep()
}


function next_step() {
    current_step = current_step + 1

    console.log(`step: change ${current_step}`)
    update_step()
}

function back_step() {
    if (current_step > 0) {
        current_step = current_step - 1
        console.log(`step: change ${current_step}`)
        update_step()
        
    } 
}

function saveCurrentStep() {
    localStorage.setItem("current_step", current_step)
}

update_step()



const selectors = document.querySelectorAll(".selector")
const card = document.getElementById("card")
let currentSelector = 0
function updateSelector() {
    selectors.forEach((selector, index) => {
        const isActive = index === currentSelector
        if (isActive) {
            console.log("Index: " + index)
        }
        selector.classList.toggle("px-8", isActive)
        selector.classList.toggle("bg-chartreuse", isActive)
        selector.classList.toggle("shadow-chartreuse", isActive)
        selector.classList.toggle("bg-white", !isActive)
        card.style.transform = `translateX(-${currentSelector * 110}%)`;
        selector.classList.toggle("hover:scale-150", !isActive)
    })
}

function setCurrentSelector(index) {
    currentSelector = index
    updateSelector()
}

updateSelector();
const updateSelectorTimer = setInterval(() => {
    const card = document.getElementById("card")
    currentSelector = (currentSelector + 1) % selectors.length
    updateSelector();
}, 3500)







