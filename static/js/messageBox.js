closeMessageDiv = document.querySelector(".closeMessageDiv");
messageBox = document.querySelector(".message__box");
closeMessageDiv.addEventListener("click", function(){
    messageBox.style.display = "none";
});

