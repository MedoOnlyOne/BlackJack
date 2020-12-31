var is_valid=false;
var shopname='';
var discount=0;
function total(){
  var items = document.getElementsByClassName("item");
  var q_form = document.getElementsByClassName("quantity_of_product");
  var lenitems = items.length;
  var total = 0;
  for(var i = 0; i < lenitems; i++){
    let price=(items[i].querySelector('span[class="q"]').innerHTML * items[i].querySelector('span[class="p"]').innerHTML)
    if (is_valid && shopname==document.getElementById('shopname').innerHTML)
        total = total + price*(100-discount)/100;
    else
        total = total + price;

    q_form[i].value = items[i].querySelector('span[class="q"]').innerHTML;
    }
  document.querySelector('#t').innerHTML = total.toFixed(2);
  document.getElementById('bill').value = total.toFixed(2);
  if(is_valid)
  {
    document.getElementById('coupon').value=document.getElementById('coupon_code').value;
  }
}

function inc(id, stock) {
    if (id.innerHTML < stock){
      id.innerHTML++;
    }
    total();
  };

function dec(id) {
    // var q = document.querySelector("#q");
    if (id.innerHTML > 0){
        id.innerHTML--;
        total();
    }
};

document.addEventListener('DOMContentLoaded', function() {
  total(); 
});
var coupon_button=document.getElementById('add_coupon');

coupon_button.addEventListener('click',function () {
    $.ajax({
        url: window.location.href,
        type: "get", //send it through get method
        data: { 
          coupon_code:document.getElementById('coupon_code').value
        },
        success: function(response) {
            is_valid=response['success'];
            if (is_valid)
            {
                discount=response['discount'];
                shopname=response['shopname'];
            }
            total();
            // alert("Discount is applied successfly for products from shop " + shopname);
        }
        ,
        error: function(xhr) {
          console.log('ERROR')
        }
      });
})
