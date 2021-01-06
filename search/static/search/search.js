var url_string=window.location.href;
var url=new URL(url_string);
console.log(url.searchParams)
var page_num;
if (url.searchParams.get('page'))
    page_num=url.searchParams.get('page');
else
    page_num='1';
var current = document.getElementById(page_num);
current.classList.add('current');
current.childNodes[0].style = "color:#BFB367";