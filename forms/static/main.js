// const e = require("express");

const spanEmail = document.getElementById("span-email");
const spanPassword = document.getElementById("span-password");

let inputEmail = document.getElementById("email");
let inputPassword = document.getElementById("password");


function addStyle(spanElement, inputElement) {
    spanElement.style =
    "font-size: 11px;color: rgb(121, 83, 133);transform: translateY(-13px);";
    inputElement.style="border-color:rgb(121, 83, 133)"
  
}

function removeStyle(spanElement, inputElement) {
    spanElement.style =
    "font-size: 13px;color: rgb(190, 190, 190);transform: translateY(0px);";
    inputElement.style="border-color: rgb(190, 190, 190)"
  
}


function addEvents(elementListening, elementTarget) {
    
    elementListening.addEventListener("focus", () => {
        addStyle(elementTarget, elementListening);
      });
      
    elementListening.addEventListener("blur", (e) => {
          if (e.target.value.length == 0){
              removeStyle(elementTarget, elementListening);
          } 
      });
      elementTarget.addEventListener('click', ()=> {
        addStyle(elementTarget, elementListening);
        elementListening.focus()
      })
}

addEvents(inputEmail, spanEmail)
addEvents(inputPassword, spanPassword)
