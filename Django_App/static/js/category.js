
const items = document.querySelectorAll(".items .item");

items.forEach((item) => {
    
    const category = document.querySelectorAll(".category button");

    if( item.className !== `item it${category[0].className}` ){
        item.style.display = "none";
    }

    for(let i=0; i<category.length; i++){
        category[i].addEventListener('click',()=>{

            const categoryName = category[i].className

            if( item.className === `item it${categoryName}` ){
                item.style.display = "block";
            } else {
                item.style.display = "none";
            }
            
        });
    }
});
