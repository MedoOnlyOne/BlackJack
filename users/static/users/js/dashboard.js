const buttons = document.querySelector('.buttonsContainer');
if (buttons.children.length==3){
    buttons.classList.add('not-seller');
    for (let button of buttons.children){
        button.classList.add('not-seller');
    }
}