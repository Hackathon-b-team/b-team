// モーダルを表示させる
const addCategoryBtn = document.getElementById("user-fix");
const addCategoryModal = document.getElementById("book-confirmation-modal");
const addCategoryCloseBtn = document.getElementById("modal-close-btn");

// モーダルを開く
function modalOpen(mode) {
  if (mode === "add-category") {
    addCategoryModal.style.display = "block";
  }
}

// <button id="add-category-btn">カテゴリーを作成</button>ボタンがクリックされた時
addCategoryBtn.addEventListener("click", () => {
  modalOpen("add-category");
});

// モーダルを閉じる
function modalClose(mode) {
  if (mode === "add-category") {
    addCategoryModal.style.display = "none";
  }
}

// モーダル内のキャンセルがクリックされた時
addCategoryCloseBtn.addEventListener("click", () => {
  modalClose("add-category");
});

// モーダルコンテンツ以外がクリックされた時
addEventListener("click", outsideClose);
function outsideClose(e) {
  if (e.target == addCategoryModal) {
    addCategoryModal.style.display = "none";
  }
}

// モーダル内のキャンセルがクリックされた時
bookCategoryCloseBtn.addEventListener("click", () => {
  modalClose("book-confirmation");
});

// モーダルコンテンツ以外がクリックされた時
addEventListener("click", outsideClose);
function outsideClose(e) {
  if (e.target == bookCategoryModal) {
    bookCategoryModal.style.display = "none";
  }
}