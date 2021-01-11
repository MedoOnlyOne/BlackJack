var first_name = document.getElementById('first_name');
var last_name = document.getElementById('last_name');
var email = document.getElementById('email');
var username = document.getElementById('username');
var address = document.getElementById('address');
var password  = document.getElementById('password');
var confirm_password = document.getElementById('confirm_password');
var code = document.getElementById('code');
var phone_num = document.getElementById('phone_num');
var country = document.getElementById('CO');
var preferred_currency = document.getElementById('PC');


function is_in_datalist(datalist,value)
{
    let option = document.querySelector("#" + datalist + " option[value='" + value + "']");
    if (option!=null)
        return option.value.length>0;
    return false;
}


function ValidateEmail(mail) 
{
    if (/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(mail))
      return (true)
    return (false)
}

function code(){
    let code = window.event.target;
    if (code.value == '' || (code.value.length>0 && code.value[0]!='+'))
        code.value='+';
}

form.elements.namedItem('code').addEventListener('input',code);


function check(){
    let first_name_working = first_name.value.length>=2; 
    let last_name_working = last_name.value.length>=2;
    let email_working = ValidateEmail(email.value);
    let username_working = username.value.length>5;
    if (first_name_working && window.event.target==first_name)
    {
        first_name.classList.add('correct');
        first_name.classList.remove('wrong');
    }
    else if (window.event.target==first_name)
    {
        first_name.classList.add('wrong');
        first_name.classList.remove('correct');
    }
    if (last_name_working && window.event.target==last_name )
    {
        last_name.classList.add('correct');
        last_name.classList.remove('wrong');
    }
    else if ( window.event.target==last_name )
    {
        last_name.classList.add('wrong');
        last_name.classList.remove('correct');
    }
    if (email_working && window.event.target==email)
    {
        email.classList.add('correct');
        email.classList.remove('wrong');
    }
    else if(window.event.target==email)
    {
        email.classList.add('wrong');
        email.classList.remove('correct');
    }
    if (username_working && window.event.target==username)
    {
        username.classList.add('correct');
        username.classList.remove('wrong');
    }
    else if (window.event.target==username)
    {
        username.classList.add('wrong');
        username.classList.remove('correct');
    }
    let address_working = form.elements.namedItem('address').value.length>5 ;
    let password_working = form.elements.namedItem('password').value.length>5;
    let confirm_password_working = form.elements.namedItem('password').value==form.elements.namedItem('confirm_password').value && form.elements.namedItem('confirm_password').value!='';
    if (address_working && window.event.target==address)
    {
        address.classList.add('correct');
        address.classList.remove('wrong');
    }
    else if ( window.event.target==address )
    {
        address.classList.add('wrong');
        address.classList.remove('correct');
    }
    if (password_working && window.event.target==password)
    {
        password.classList.add('correct');
        password.classList.remove('wrong');
    }
    else if ( window.event.target==password )
    {
        password.classList.add('wrong');
        password.classList.remove('correct');
    }
    if (confirm_password_working && window.event.target==confirm_password)
    {
        confirm_password.classList.add('correct');
        confirm_password.classList.remove('wrong');
    }
    else if (window.event.target==confirm_password)
    {
        confirm_password.classList.add('wrong');
        confirm_password.classList.remove('correct');
    }
    let code = form.elements.namedItem('code');
    let code_working = code.value.length>=2 && !isNaN(code.value.slice(1))
    let phone_working = form.elements.namedItem('phone_num').value.length > 4;
    
    if (code_working && window.event.target==code)
    {
        code.classList.add('correct');
        code.classList.remove('wrong');
    }
    else if (window.event.target==code)
    {
        code.classList.add('wrong');
        code.classList.remove('correct');
    }
    if (phone_working && window.event.target==phone_num)
    {
        phone_num.classList.add('correct');
        phone_num.classList.remove('wrong');
    }
    else if (window.event.target==phone_num)
    {
        phone_num.classList.add('wrong');
        phone_num.classList.remove('correct');
    }
    
    let country_working=is_in_datalist('countries',country.value);
    let preferred_currency_working = is_in_datalist('Preferred_Currency',preferred_currency.value);
    if (country_working && window.event.target==country)
    {
        country.classList.add('correct');
    }
    if (preferred_currency_working && window.event.target==preferred_currency)
    {
        preferred_currency.classList.add('correct');
    }

    if(first_name_working && last_name_working && email_working && username_working && address_working && password && password_working && confirm_password_working && code_working && phone_working && country_working && preferred_currency_working)
        document.getElementById('signup_btn').disabled=false;
    else
        document.getElementById('signup_btn').disabled=true;

}


var inputs = document.getElementsByTagName('input');
for(let i=0;i<inputs.length;i++){
    if (inputs[i].name!='csrfmiddlewaretoken')
        inputs[i].addEventListener('input',check);
}