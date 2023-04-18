const inpFile = document.getElementById('id_main_image');
const previewImage = document.querySelector('.main_preview_img');
const previewText = document.querySelector('.main_preview_span');
const cancelBtn = document.getElementById('cancel-btn');

inpFile.addEventListener("change", function() {
    var mainImagesURL = document.getElementById("main_preview_img").src
    const file = this.files[0];

    if (file) {
        const reader = new FileReader();

        previewText.style.display = "none";
        previewImage.style.opacity = 1;
        cancelBtn.style.display = "block";

        reader.onload = function(){
            const result = reader.result;
            previewImage.src = result;
        }
        cancelBtn.addEventListener("click", function(){
            previewImage.src = mainImagesURL;
            inpFile.value = null;
            previewText.style.display = "flex";
            cancelBtn.style.display = "none";
        });
        reader.readAsDataURL(file);
    }
});

const inpFile2 = document.getElementById('id_image');
const container2 = document.getElementById('extra_image_preview');
//const previewImage2 = document.querySelector('.extra_preview_img');
const wrapBefore = document.querySelector('.before_upload');
const wrapAfter = document.querySelector('#after_upload');
const images_container = document.querySelector('#images_container');
const second_images_container = document.getElementById('second_images_container')
const previewText2 = document.querySelector('.extra_preview_span');
const cancelBtn2 = document.getElementById('cancel-btn2');

inpFile2.addEventListener("change", function() {
//    extraImagesURL = document.getElementsByClassName("extra_preview_img")
//    console.log(extraImagesURL)
//    reservedFiles = []
//    for(i in extraImagesURL){
//        console.log(i)
//        reservedFiles.push(i)
//    }
//    console.log(reservedFiles)
    const file2 = this.files;
    wrapBefore.style.display = "none";
    wrapAfter.style.display = "grid";
    images_container.style.display = "grid";
    cancelBtn2.style.display = "block";
    for(i of inpFile2.files){
        let reader = new FileReader();
        let figure = document.createElement("div");
        let figcap = document.createElement("figcaption");
        let figcapholder = document.createElement("div");
        figcap.innerText = i.name;
        reader.onload=()=>{
            images_container.style.display = "none";
            second_images_container.style.display = "grid";
            let img = document.createElement("img");
            img.setAttribute("src",reader.result);
            img.setAttribute("class", "extra_preview_img");
            figure.setAttribute("class", "holder2");
            figcapholder.setAttribute("class", "figcapholder");
            figcap.setAttribute("class", "figcap");
            second_images_container.appendChild(figure);
            figure.appendChild(img);
            figcapholder.appendChild(figcap);
            figure.appendChild(figcapholder);
        }
//    previewImage2 = document.querySelectorAll('.extra_preview_img');
    cancelBtn2.addEventListener("click", function(){
        second_images_container.style.display = "none"
//        previewImage2 = document.querySelectorAll('.extra_preview_img');
        let holders = document.querySelectorAll('.holder2');
        console.log("not done!")
//        for(i of previewImage2){
//            i.src = '';
//            console.log("done!")
//        }
        holders.forEach(holder => {
            holder.remove();
            console.log("also done!")
        });
        inpFile2.value = null;
        document.getElementById("images_container").style.display = "grid";
        previewText2.style.display = "block";
        cancelBtn2.style.display = "none";
        wrapAfter.style.display = "none";
//        wrapAfter.style.display = "none";
        wrapBefore.style.display = "flex";

    });
    reader.readAsDataURL(i)
}
//    var images = []
//    if (file2) {
//        for (i = 0;i < file2.length; i++) {
//
//        }
//        const reader2 = new FileReader();
//
//        previewImage2.style.opacity = 1;
//        cancelBtn2.style.display = "block";
//        wrapAfter.style.display = "grid";
//        wrapBefore.style.display = "none";
//
//        reader2.onload = function(){
//            const result2 = reader2.result;
//            previewImage2.src = result2;
//        }
//        cancelBtn2.addEventListener("click", function(){
//            previewImage2.src = '';
//            previewImage2.style.width = "100px";
//            previewImage2.style.height = "100px";
//            inpFile2.value = null;
//            previewText2.style.display = "block";
//            cancelBtn2.style.display = "none";
//            wrapAfter.style.display = "none";
//            wrapBefore.style.display = "flex";
//
//        });
//        reader2.readAsDataURL(file2);
//    }
});

var expanded = false;
const select = document.getElementById("select");
const plusButton = document.getElementById("new_option")
const addButton = document.getElementById("add_category")
var checkboxes = document.getElementById("checkboxes");

select.addEventListener("click", function() {
    if (!expanded) {
      checkboxes.style.display = "block";
      plusButton.style.display = "none";
      addButton.style.display = "none";
      expanded = true;
    } else {
      checkboxes.style.display = "none";
      plusButton.style.display = "block";
      addButton.style.display = "block";
      expanded = false;
    }
});

const available = document.getElementById("available")
var repeated_txt = false;

addButton.addEventListener("click", function(){
    var optText = document.getElementById("new_option").value;
    var texts = document.getElementsByClassName("options_txt");
    optText = optText.replace(/^\s+/, '').replace(/\s+$/, '');

    invalid_txt = false;
    for (var i = 0, len = texts.length; i < len; i++) {
        if (texts[i].innerHTML == optText) {
            invalid_txt = true;
            alert("category added already!")
            break
        } else {
            invalid_txt = false;
        }
    }
    if (optText == '') {
        invalid_txt = true;
        alert("invalid category input!")
    }

    if (optText.length > 20){
        invalid_txt = true;
        alert("maximum number of characters is 20 for categorys")
    }
    if (!invalid_txt) {
        if (available) {
            available.style.display = "none";
        }
        var newOptText = document.createTextNode(optText);
        var newcheck = document.createElement("input");
        var newOpt = document.createElement("label");
        var newdiv = document.createElement("div");

        newOpt.setAttribute("for", optText);
        newOpt.setAttribute("class", "options_txt");

        newcheck.setAttribute("type", "checkbox");
        newcheck.setAttribute("checked", "");
        newcheck.setAttribute("value", optText);
        newcheck.setAttribute("name", "category");
        newcheck.setAttribute("class", "checkbox_cat");

        newdiv.setAttribute("class", "options");

        checkboxes.insertBefore(newdiv, checkboxes.firstChild);
        newdiv.appendChild(newOpt);
        newdiv.appendChild(newcheck)
        newOpt.appendChild(newOptText);
        optText.value = '';
    }
});

const nameinp = document.getElementById("id_name");
nameinp.addEventListener("focusout", function(){
    var text = this.value;
    text = text.replace(/\s/g, "");
    var letters = /^[A-Za-z]+$/;
    if (!text.match(letters))
    alert("you should only use letters as the name of the product!");
    return false;
});
