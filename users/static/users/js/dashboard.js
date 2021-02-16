const buttons = document.querySelector('.buttonsContainer');
const confirmButton = document.querySelector('#ConfirmButton');
if (buttons.children.length==3){
    buttons.classList.add('not-seller');
    for (let button of buttons.children){
        button.classList.add('not-seller');
    }
}

function enable(input_id) {
    if (confirmButton.disabled==true)
        confirmButton.disabled=false;
    document.getElementById(input_id).disabled = false;
}  

function enableAll() {
  let inputs, i;
  inputs = document.getElementsByTagName('input');
  for (i = 0; i < inputs.length; ++i) {
      inputs[i].disabled = false;
  }
}