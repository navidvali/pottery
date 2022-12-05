function delete_product (product_id) {
    $.ajax({
        url: "/users/admin_panel_delete",
        data: {"product_id":product_id},
        success: function(){
        }
    })
}


$(document).ready(function(){
//     setInterval(function(){
        console.log("1")
        $.ajax({
            Type: 'GET',
            url: "/users/admin_panel_products",
            success: function(response){
                var product = document.getElementsByClassName('products_wrap')[0];
                $(".products_container").empty()
                console.log("success")
                console.log(product)
                for(var i in response.products){
                    console.log("for")
                    var clone = product.cloneNode(true);
                    clone.getElementsByClassName("products_name")[0].innerHTML = response.products[i].name;
                    clone.getElementsByClassName("products_image")[0].src = response.products[i].main_image;
                    clone.getElementsByClassName("delete_btn")[0].value = response.products[i].product_id;
                    clone.getElementsByClassName("edit_link")[0].href = "/users/admin_panel_edit/" + response.products[i].product_id;
                    $(".products_container").append(clone)
                };
                document.querySelectorAll('.delete_btn').forEach(item => {
                    item.addEventListener("click", function(){
                    delete_product(item.value)
                })
            })
            }
        })
//     },1000)
});

console.log("0")

// document.querySelector('.delete_btn').addEventListener('click', function(){
    
//     data = 
//     $.ajax ({
//     Type: 'GET',
//     url: "/users/admin_panel",
//     data : {"searchInput":searchInput},
//     success: function (response) {

// });

