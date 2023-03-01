// モーダルを表示させる
const changeUserBtn = document.getElementById("user-fix");
const changeUserModal = document.getElementById("user-confirmation-modal");
const changeUserCloseBtn = document.getElementById("modal-close");

// モーダルを開く
// function modalOpen(mode) {
//   if (mode === "user-change") {
//     changeUserModal.style.display = "block";
//   }
// }

// <button id="add-category-btn">カテゴリーを作成</button>ボタンがクリックされた時
changeUserBtn.addEventListener("click", () => {
  changeUserModal.style.display = "block";
});

// モーダルを閉じる
// function modalClose(mode) {
//   if (mode === "user-change") {
//     changeUserModal.style.display = "none";
//   }
// }

// モーダル内のキャンセルがクリックされた時
changeUserCloseBtn.addEventListener("click", () => {
  changeUserModal.style.display = "none";
});

// モーダルコンテンツ以外がクリックされた時
addEventListener("click", outsideClose);
function outsideClose(e) {
  if (e.target == changeUserModal) {
    changeUserModal.style.display = "none";
  }
}