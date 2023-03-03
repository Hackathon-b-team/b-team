// モーダルを表示させる

const addCategoryBtn = document.getElementById("add-category-btn");
const addCategoryModal = document.getElementById("add-category-modal");
const addCategoryCloseBtn = document.getElementById("add-category-close-btn");

// <button id="add-category-btn">カテゴリーを作成</button>ボタンがクリックされた時
addCategoryBtn.addEventListener("click", () => {
  // モーダルを開く
  addCategoryModal.style.display = "block";
});

// モーダル内のキャンセルがクリックされた時
addCategoryCloseBtn.addEventListener("click", () => {
  // モーダルを閉じる
  addCategoryModal.style.display = "none";
});

// モーダルコンテンツ以外がクリックされた時
addEventListener("click", outsideClose);
function outsideClose(e) {
  if (e.target == addCategoryModal) {
    addCategoryModal.style.display = "none";
  }
}