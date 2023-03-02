// モーダルを表示させる
const changeUserBtn = document.getElementById("user-fix");
const changeUserModal = document.getElementById("user-confirmation-modal");
const changeUserCloseBtn = document.getElementById("modal-close");


// <button id="add-category-btn">カテゴリーを作成</button>ボタンがクリックされた時
changeUserBtn.addEventListener("click", () => {
  changeUserModal.style.display = "block";
});

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

// 入力後のフォームの色を変更
const input = document.getElementById("id_username");
input.addEventListener("input", () => {
  input.style.backgroundColor = "rgb(232, 240, 254)";
});
const input2 = document.getElementById("id_email");
input2.addEventListener("input", () => {
  input2.style.backgroundColor = "rgb(232, 240, 254)";
});
