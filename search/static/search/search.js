var url_string=window.location.href;
var url=new URL(url_string);
var search = document.getElementById('s');
var search_btn = document.getElementById('b');
var page_num;
if (url.searchParams.get('page'))
    page_num=url.searchParams.get('page');
else
    page_num='1';
var current = document.getElementById(page_num);
if (current != null){
    current.classList.add('current');
    current.childNodes[0].style = "color:#BFB367";
}

search.addEventListener('input',function(){
    if (search.value.length>0){
        search_btn.disabled=false;
    }
    else{
        search_btn.disabled=true;
    }
});