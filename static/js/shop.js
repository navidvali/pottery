const categoryWrap = document.getElementById('category_btn');
const dropdownContent = document.getElementById('dropdown-content');
var expanded = false;

categoryWrap.addEventListener("click", function() {
    if (!expanded) {
      dropdownContent.style.display = "grid";
      expanded = true;
    } else {
      dropdownContent.style.display = "none";
      expanded = false;
    }
});
//categoryWrap.addEventListener('click', function(){
//    var activate = True
//
//    dropdownContent.style.display = "grid";
//});

SelectedCategories = [];
document.querySelectorAll('.category_checkbox').forEach(item => {
    item.addEventListener('change', event => {
        if (item.checked) {
            SelectedCategories.push(item.id);
        } else {
            const indexOfObject = SelectedCategories.findIndex(category => {
                return category === item.id;
            });
            SelectedCategories.splice(indexOfObject, 1);
        }

        if (!SelectedCategories.length) {
            location.reload()
        }
    $.ajax ({
        Type: 'GET',
        url: "/shop/category_filter",
        data: {'SelectedCategories': SelectedCategories},
        success: function (response) {
            console.log(response.filtered_products)
//            $(".products_field").html(response.data)
            var product = document.getElementsByClassName('product-link')[0];
            $("#products_field").empty()
            $(".page_num").remove()
            console.log(response.filtered_products)
            for(var i in response.filtered_products){
                var clone = product.cloneNode(true);
                clone.href = "/shop/view_product/" + response.filtered_products[i].product_id;
                clone.getElementsByClassName("product-name")[0].innerHTML = response.filtered_products[i].name;
                clone.getElementsByClassName("product-price")[0].innerHTML = response.filtered_products[i].price + "$";
                clone.getElementsByClassName("product-image")[0].src = response.filtered_products[i].main_image;
                $("#products_field").append(clone)
            }
        }
    })
  })
})

const searchButton = document.getElementById('search_button');

searchButton.addEventListener("click", function(){

    var notFoundText = document.getElementById("not_found_text")
    if(notFoundText){
        notFoundText.remove()
    }
    let searchInput = document.getElementById('search_input').value
    searchInput = searchInput.replace(/^\s+/, '').replace(/\s+$/, '');

    if (searchInput) {
        $.ajax ({
            Type: 'GET',
            url: "/shop/search_product",
            data : {"searchInput":searchInput},
            success: function (response) {
                if(response.product[0]){
                    console.log(response.product)
                    var product = document.getElementsByClassName('product-link')[0];
                    $("#products_field").empty()
                    $(".page_num").remove()
                    for(var i in response.product){
                        var clone = product.cloneNode(true);
                        clone.href = "/shop/view_product/" + response.product[i].product_id;
                        console.log(response.product[i].name)
                        clone.getElementsByClassName("product-name")[0].innerHTML = response.product[i].name;
                        clone.getElementsByClassName("product-price")[0].innerHTML = response.product[i].price + "$";
                        clone.getElementsByClassName("product-image")[0].src = "/media/" + response.product[i].main_image;
                        $("#products_field").append(clone)
                    }
                }else{
                    var para = document.createElement("p");
                    para.innerText = "couldn't find the product you're looking for ";
                    para.id = "not_found_text";
                    $("#dropdown").after(para);
                }
            }
        });
    };
});
