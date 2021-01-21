var menu_open=false;
const sidemenu=document.getElementsByClassName('sidemenu')[0];
const header=document.getElementsByTagName('header')[0];
const burgers=document.getElementsByClassName('burgers')[0];
const main=document.getElementsByTagName('main')[0];
const wrapper=document.getElementsByClassName('wrapper')[0];
const mobile=document.querySelector('.mobile-nav');
const search_input=document.querySelector('.search-field');
const search_bar=document.querySelector('.search-bar');
document.addEventListener('click', function(event){
    if(!sidemenu.contains(event.target) && menu_open && event.target!=burgers && !burgers.contains(event.target)){
        for(let i=0;i<burgers.children.length;i++)
        {   
            burgers.children[i].classList.remove('clicked');
        }
        sidemenu.classList.remove('shown');
        main.classList.remove('shrink');
        wrapper.classList.remove('grey-out');
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
        wrapper.classList.add('grey-out');
        mobile.classList.add('open');
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
        wrapper.classList.remove('grey-out');
        mobile.classList.remove('open');
        menu_open=false;
    }
})

function resize(){
    const body=document.querySelector('body');
    if (header.clientHeight+main.clientHeight<body.clientHeight)
        document.querySelector('.wrapper').style=`height:${body.clientHeight}px`;
    else
        document.querySelector('.wrapper').style=`height:${header.clientHeight+main.clientHeight+6}px`;
}

const resizeObserver = new ResizeObserver(entries =>{
    console.log(entries[0].target.clientHeight);
    resize();
})
  
  // start observing a DOM node
  resizeObserver.observe(main);
  
document.addEventListener('click',function(){
    console.log(document.activeElement);
    if (search_input===document.activeElement){
        search_bar.classList.add('focused');
    }
    else{
        search_bar.classList.remove('focused');
    }
})

