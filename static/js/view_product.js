//var colors = ["#6CC2BD","#5A819E","#7D7AA2","#F67E7D","#FFC1A7","#FFE5C4","#7F395E","#5E183D","#0B022C"];
//var category = document.getElementsByClassName("category");
//
//for (var i = 0, len = category.length; i < len; i++) {
//    var random_color = colors[Math.floor(Math.random() * colors.length)];
//    category[i].style.backgroundColor = random_color;
//}

var pictures = document.getElementsByClassName("extra_image");
var active = document.getElementsByClassName("active");

for (var i=0; i < pictures.length; i++){
    pictures[i].addEventListener('click', function(){
        if (active.length > 0){
            active[0].classList.remove('active')
        }

        var main_img = document.getElementById('main_img');
        var pocket = '';
        this.classList.add('active');
        pocket = main_img.src;
        main_img.src = this.src;
        this.src = pocket;
    })
}

var arrowRight = document.getElementById("rightarrow");
var arrowLeft = document.getElementById("leftarrow");

arrowLeft.addEventListener("click", function(){
	document.getElementById("sliders_images").scrollLeft -= 150;;
})

arrowRight.addEventListener("click", function(){
  document.getElementById("sliders_images").scrollLeft += 150;
})

//// to search the category when clicked on
//document.querySelectorAll('.search_link').forEach(item => {
//    item.addEventListener("click", event => {
//         $.ajax ({
//             Type: 'GET',
//             url: "/shop/category_filter",
//             data: {'SelectedCategories': [item.id]},
//             success: function (response) {
//                 console.log(response.filtered_products)
//             }
//         })
//    })
//});


document.querySelector(".add_to_cart").addEventListener("click", function() {

    this.style.display = "none"
    document.querySelector(".added").style.display = "block"
//    num = document.querySelector("#num_in_cart").innerHTML;
//    num = parseInt(num)
//    document.querySelector("#num_in_cart").innerHTML = num + 1
    $.ajax ({
        Type: 'GET',
        url: "/users/add_to_cart",
        data : {"product_id": this.id},
        success: function (response) {
            let x = document.getElementById("num_of_orders").innerHTML
            document.getElementById("num_of_orders").innerHTML = parseInt(x) + 1
        }
    })
});





