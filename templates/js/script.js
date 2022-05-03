const name = document.getElementById("my-name");
const button = document.getElementById("show-my-name-btn");

button.addEventListener("click", () => {
    name.textContent = "JOHN CENA";
})