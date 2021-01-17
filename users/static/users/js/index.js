var menu_open=false
const sidemenu=document.getElementsByClassName('sidemenu')[0];
const burgers=document.getElementsByClassName('burgers')[0];
const main=document.getElementsByTagName('main')[0];
document.addEventListener('click', function(event){
    if(!sidemenu.contains(event.target) && menu_open && event.target!=burgers && !burgers.contains(event.target)){
        for(let i=0;i<burgers.children.length;i++)
        {   
            burgers.children[i].classList.remove('clicked');
        }
        sidemenu.classList.remove('shown');
        main.classList.remove('shrink');
        menu_open=false;
    }
})
burgers.addEventListener('click', function() {
    if(!menu_open)
    {
        for(let i=0;i<burgers.children.length;i++)
        {   
            burgers.children[i].classList.add('clicked');
        }
        sidemenu.classList.add('shown');
        main.classList.add('shrink');
        menu_open=true;
    }
    else
    {
        for(let i=0;i<burgers.children.length;i++)
        {   
            burgers.children[i].classList.remove('clicked');
        }
        main.classList.remove('shrink');
        sidemenu.classList.remove('shown');
        menu_open=false;
    }
})