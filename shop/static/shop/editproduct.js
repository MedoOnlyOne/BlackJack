var product_name = document.getElementById('product_name');
var stock = document.getElementById('stock');
var price = document.getElementById('price');
var description = document.getElementById('description');
var button = document.getElementById('submit_btn');

fn =function(){
    if (product_name.value.length>=5 && stock.value!='' && description.value.length>=15)
        {
            button.disabled=false;
        }
        else
        {
            button.disabled=true;
        }
}

document.addEventListener('DOMContentLoaded', function() {
    fn(); 
  });

product_name.addEventListener('input',fn);
stock.addEventListener('input',fn);
price.addEventListener('input',fn);
description.addEventListener('input',fn);