
let num=[];
// トータル金額算出用
let total_init=0;
let total=[0,0,0,0,0,0,0,0,0,0,0,0];
// 金額をどこまで反映させるかのカウント
let count=[0,0,0,0,0,0,0,0,0,0,0,0];
// 最後に表示される行の算出用
let final_init=[];
let final=[];

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
items.forEach((item, index) => {
    
    const category = document.querySelectorAll(".category button");
    const totalId = document.getElementById("total");

    // 本ページに遷移したときの処理
    if( item.className !== `item it${category[0].className}` ){
        item.style.display = "none";
    } else {
        num = item.innerText.match(/\d+/g);
        total_init += Number(num[num.length-1]);
        item.setAttribute("id",`final${index}`);
        if(final_init[0]){
            items[final_init[0]-1].setAttribute("id","");
        }
        final_init[0] = index + 1;
    }

    category[0].style.color = "#155E75";
    category[0].style.backgroundColor = "#EBEBEB";

    // タグがクリックされた時の処理
    for(let j=0; j<category.length; j++){
        category[j].addEventListener('click',()=>{

            const categoryName = category[j].className;

            // 色付け
            category[j].style.color = "#155E75";
            category[j].style.backgroundColor = "#EBEBEB";
            for(let k=0; k<category.length; k++){
                if( k !== j ){
                    category[k].style.color = "#BEBEBE";
                    category[k].style.backgroundColor = "#FFFFFF";
                }
            }

            // 表示、合計金額、最後の行算出処理
            if( count[j] < items.length){
                if( item.className === `item it${categoryName}` ){
                    item.style.display = "table-row";
                    num = item.innerText.match(/\d+/g);
                    total[j] += Number(num[num.length-1]);
                    item.setAttribute("id",`final${index}`);
                    if(final[j]){
                        items[final[j]-1].setAttribute("id","");
                    }
                    final[j] = index + 1;
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
            console.log(final)
        });
    }
    totalId.innerHTML = total_init+"円";
});
