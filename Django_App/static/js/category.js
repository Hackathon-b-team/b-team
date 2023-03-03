
const items = document.querySelectorAll(".items .item");

items.forEach((item) => {
    
    const category = document.querySelectorAll(".category button");

    if( item.className !== `item it${category[0].className}` ){
        item.style.display = "none";
    }

    category[0].style.color = "#155E75";
    category[0].style.backgroundColor = "#EBEBEB";

    for(let i=0; i<category.length; i++){
        category[i].addEventListener('click',()=>{

            const categoryName = category[i].className

            category[i].style.color = "#155E75";
            category[i].style.backgroundColor = "#EBEBEB";
            for(let j=0; j<category.length; j++){
                if( j !== i ){
                    category[j].style.color = "#BEBEBE";
                    category[j].style.backgroundColor = "#FFFFFF";
                }
            }

            if( item.className === `item it${categoryName}` ){
                item.style.display = "block";
            } else {
                item.style.display = "none";
            }
            
        });
    }
});
