// モーダルを表示させる
const logoutBtn = document.getElementById("logout-modal");
const logoutModal = document.getElementById("logout-confirmation-modal");
const logoutCloseBtn = document.getElementById("logout-modal-close");

// モーダルを開く
// function modalOpen(mode) {
//   if (mode === "bt-logout") {
//     logoutModal.style.display = "none";
//   }
// }

// <button id="add-category-btn">カテゴリーを作成</button>ボタンがクリックされた時
logoutBtn.addEventListener("click", () => {
  logoutModal.style.display = "block";
});

// モーダルを閉じる
// function modalClose(mode) {
//   if (mode === "bt-logout") {
//     logoutModal.style.display = "none";
//   }
// }

// モーダル内のキャンセルがクリックされた時
logoutCloseBtn.addEventListener("click", () => {
  logoutModal.style.display = "none";
});

// モーダルコンテンツ以外がクリックされた時
addEventListener("click", outsideClose);
function outsideClose(e) {
  if (e.target == logoutModal) {
    logoutModal.style.display = "none";
  }
}