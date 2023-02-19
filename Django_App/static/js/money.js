
const items = document.querySelectorAll(".items .item");
let num=[];
let total_init=0;
// トータル金額算出用
let total=[0,0,0,0,0,0,0,0,0,0,0,0];
// 金額をどこまで反映させるかのカウント
let count=[0,0,0,0,0,0,0,0,0,0,0,0];

items.forEach((item) => {
    
    const category = document.querySelectorAll(".category button");
    const totalId = document.getElementById("total");

    // 本ページに遷移したときの処理
    if( item.className !== `item it${category[0].className}` ){
        item.style.display = "none";
    } else {
        num = item.innerText.match(/\d+/g);
        total_init += Number(num[num.length-1]);
    }

    // タグがクリックされた時の処理
    for(let i=0; i<category.length; i++){
        category[i].addEventListener('click',()=>{

            const categoryName = category[i].className;

            if( count[i] < items.length){
                if( item.className === `item it${categoryName}` ){
                    item.style.display = "table-row";
                    num = item.innerText.match(/\d+/g);
                    total[i] += Number(num[num.length-1]);
                } else {
                    item.style.display = "none";
                }
                flag = "False";
            } 
            else {
                if( item.className === `item it${categoryName}` ){
                    item.style.display = "table-row";
                } else {
                    item.style.display = "none";
                }
            }
            totalId.innerHTML = total[i]+"円";
            count[i]++;
        });
    }
    totalId.innerHTML = total_init+"円";
});
