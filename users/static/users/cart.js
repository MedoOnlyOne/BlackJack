var is_valid=false;
var shopname='';
var discount=0;
var type='shop';
var old = document.getElementsByClassName('old_price');
var neww = document.getElementsByClassName('new_price')
function total(){
  var items = document.getElementsByClassName("item");
  var q_form = document.getElementsByClassName("quantity_of_product");
  var shopnames = document.getElementsByClassName("shopname");
  var lenitems = items.length;
  var total = 0;
  for(var i = 0; i < lenitems; i++){
    let price = (items[i].querySelector('span[class="q"]').innerHTML * items[i].querySelector('span[class="p"]').innerHTML); 
    if (is_valid && (type=='user' || type=='event' ||shopname==shopnames[i].innerHTML))
    {
      total = total + price*(100-discount)/100;
      neww[i].querySelector('span').innerHTML = price*(100-discount)/100;
    }
    else
    {
        total = total + price;
        neww[i].querySelector('span').innerHTML = price ;
    }
    q_form[i].value = items[i].querySelector('span[class="q"]').innerHTML;
  }
  document.querySelector('#t').innerHTML = total.toFixed(2);
  document.getElementById('bill').value = total.toFixed(2);
  if(is_valid)
  {
    document.getElementById('coupon').value=document.getElementById('coupon_code').value;
    console.log(old);
    for(let item of old)
    {
      item.style="text-decoration:line-through;"
    }
    for(let item of neww)
    {
      item.style="visibility:visible;"
    }
  }
  else{
    for(let item of old)
    {
      item.style="text-decoration:none;"
    }
    for(let item of neww)
    {
      item.style="visibility:hidden;"
    }
  }
}

function inc(id, stock) {
    id=document.getElementById(id);
    console.log(id);
    if (id.innerHTML < stock){
      id.innerHTML++;
    }
    total();
  };

function dec(id) {
    id=document.getElementById(id);
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
              else if (response['type']=='event')
              {
                discount=response['discount'];
                type=response['type'];
                alert('Event Coupon entered successfully');
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
// // // // // 