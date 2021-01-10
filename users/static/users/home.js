var catheads = document.getElementsByClassName('cathead');
var cur = document.getElementById('cur');
var cats = document.getElementsByClassName('cat');
var cur_cat = document.getElementById('cur_cat');
var search = document.getElementById('s');
var search_btn = document.getElementById('b');


for(let i=0;i<catheads.length;i++){
    catheads[i].children[0].addEventListener('click',function(){
        cur.id='';
        window.event.target.id='cur';
        cur=window.event.target;
        let current_category=cur.innerHTML;
        for(let i=0;i<6;i++){
            if (cats[i].children[0].innerHTML==current_category)
                cats[i].style="display:block";
            else
                cats[i].style="display:none";
    }
    });
}

search.addEventListener('input',function(){
    if (search.value.length>0){
        search_btn.disabled=false;
    }
    else{
        search_btn.disabled=true;
    }
});
window.onload = init;
