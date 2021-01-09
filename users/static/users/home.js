var catheads = document.getElementsByClassName('cathead');
var cur = document.getElementById('cur');
var cats = document.getElementsByClassName('cat');


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


document.addEventListener('DOMContentLoaded',function(){
    for(let i=1;i<6;i++)
        cats[i].style="display:none";
})