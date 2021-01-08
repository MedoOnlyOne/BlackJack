var is_valid=false;
var shopname='';
var discount=0;
var type='shop';
function total(){
  var items = document.getElementsByClassName("item");
  var q_form = document.getElementsByClassName("quantity_of_product");
  var shopnames = document.getElementsByClassName("shopname");
  var lenitems = items.length;
  var total = 0;
  for(var i = 0; i < lenitems; i++){
    let price=(items[i].querySelector('span[class="q"]').innerHTML * items[i].querySelector('span[class="p"]').innerHTML);
    if (is_valid && (type=='user' || shopname==shopnames[i].innerHTML))
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
        type: "get", 
        data: { 
          coupon_code:document.getElementById('coupon_code').value
        },
        success: function(response) {
            is_valid=response['success'];
            if (is_valid)
            {
              if (response['type']=='user')
              {
                discount=response['discount'];
                type=response['type'];
                alert('User Coupon entered successfully');
              }
              else{
                discount=response['discount'];
                shopname=response['shopname'];
                type=response['type'];
                alert('Coupon successfully entered for shop '+shopname);
              }
            }
            else
            {
              alert('Invalid coupon');  
            }
            total();
        }
        ,
        error: function(e) {
          console.log('ERROR!',e);
        }
      });
})
