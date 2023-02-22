
let num=[];
let total_init=0;
// トータル金額算出用
let total=[0,0,0,0,0,0,0,0,0,0,0,0];
// 金額をどこまで反映させるかのカウント
let count=[0,0,0,0,0,0,0,0,0,0,0,0];

// 日付処理
const dates = document.querySelectorAll(".date");
let date = dates[0].innerText;
for(let i=1; i<dates.length; i++){
    if( date === dates[i].innerText ){
        dates[i].innerText = "";
    } else {
        date = dates[i].innerText;
    }
}

// 表示、金額算出処理
const items = document.querySelectorAll(".items .item");
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
    for(let j=0; j<category.length; j++){
        category[j].addEventListener('click',()=>{

            const categoryName = category[j].className;

            if( count[j] < items.length){
                if( item.className === `item it${categoryName}` ){
                    item.style.display = "table-row";
                    num = item.innerText.match(/\d+/g);
                    total[j] += Number(num[num.length-1]);
                } else {
                    item.style.display = "none";
                }
            } 
            else {
                if( item.className === `item it${categoryName}` ){
                    item.style.display = "table-row";
                } else {
                    item.style.display = "none";
                }
            }
            totalId.innerHTML = total[j]+"円";
            count[j]++;
        });
    }
    totalId.innerHTML = total_init+"円";
});
