var product_name = document.getElementById('product_name');
var stock = document.getElementById('stock');
var price = document.getElementById('price');
var image = document.getElementById('fileToUpload');
var description = document.getElementById('description');
var button = document.getElementById('submit_btn');

fn =function(){
    if (product_name.value.length>5 && stock.value!='' && description.value.length>15 && image.value!='' )
        {
            button.disabled=false;
        }
        else
        {
            button.disabled=true;
        }
}

product_name.addEventListener('input',fn);
stock.addEventListener('input',fn);
price.addEventListener('input',fn);
image.addEventListener('input',fn);
description.addEventListener('input',fn);


