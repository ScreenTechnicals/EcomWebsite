const closeImageForm = document.querySelector(".closeImageForm");
const uploadImageForm = document.querySelector(".upload_image_form");
const imageContainer = document.querySelector(".image__container");
closeImageForm.addEventListener("click", function() {
  uploadImageForm.style.display = "none";
});
imageContainer.addEventListener("click", function() {
  uploadImageForm.style.display = "block";
});

const addressEdit = document.querySelector(".address_edit");
const addressUpload = document.querySelector(".address_upload");
const closeAddressForm = document.querySelector(".closeAddressForm");
addressEdit.addEventListener("click", function() {
  addressUpload.style.display = "flex";
});
closeAddressForm.addEventListener("click", function() {
  addressUpload.style.display = "none";
});

const btnNone = document.querySelectorAll(".btn__none");
const closeMenuWarning = document.querySelector(".closeMenuWarning");
const warningNoOrder = document.querySelector(".warning_no_order");
btnNone.forEach(function (btn) {
  btn.addEventListener("click", function () {
    warningNoOrder.style.display = "block";
  });
});
closeMenuWarning.addEventListener("click", function () {
  warningNoOrder.style.display = "none";
});