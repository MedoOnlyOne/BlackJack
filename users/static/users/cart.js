var is_valid=false;
var shopname='';
var discount=0;
function total(){
  var items = document.getElementsByClassName("item");
  var lenitems = items.length;
  var total = 0;
  for(var i = 0; i < lenitems; i++){
    let price=(items[i].querySelector('span[name="q"]').innerHTML * items[i].querySelector('span[name="p"]').innerHTML)
    if (is_valid && shopname==document.getElementById('shopname').innerHTML)
        total = total + price*(100-discount)/100;
    else
        total = total + price;
    }
  document.querySelector('#t').innerHTML = total;
  document.getElementById('bill').value=total;
}

function inc(name) {
    name.innerHTML++;
    total();
  };

function dec(name) {
    // var q = document.querySelector("#q");
    if (name.innerHTML > 0){
        name.innerHTML--;
        total();
    }
};

document.addEventListener('DOMContentLoaded', function() {
  total(); 
});
var coupon_button=document.getElementById('add_coupon');

coupon_button.addEventListener('click',function () {
    // let request=new XMLHttpRequest();
    // request.open('GET',window.location.href,true);
    // request.setRequestHeader("Content-Type", "application/json;");
    // request.setRequestHeader('X-Requested-With', 'XMLHttpRequest') ;
    // coupon_code=document.getElementById('coupon_code').value
    // request.send({coupon_code:coupon_code});
    $.ajax({
        url: window.location.href,
        type: "get", //send it through get method
        data: { 
          coupon_code:document.getElementById('coupon_code').value
        },
        success: function(response) {
            console.log(response)
            is_valid=response['success']
            if (is_valid)
            {
                discount=response['discount'];
                shopname=response['shopname']
            }
            total();
        }
        ,
        error: function(xhr) {
          console.log('ERROR')
        }
      });
})
