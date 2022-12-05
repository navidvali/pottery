function no_orders(){
    container = document.getElementById("products_container")
    if (container.querySelector(".products_wrap") == null) {
        document.getElementById("no_order").style.display = "block"
        document.getElementById("products_container").style.display = "none"
        document.getElementById("sub_button").style.display = "none"
        container.style.display = "none"
    }
}

$(document).ready(no_orders())

document.querySelectorAll('.delete_btn').forEach(item => {
    item.addEventListener("click", function(){
        $.ajax ({
            Type: 'GET',
            url: "/users/delete_order/",
            data: {'productuser_id': item.id},
            success: function (response) {
                item.closest('div').parentElement.closest('div').remove()
                let x = document.getElementById("total").innerText
                let total_price = parseFloat(x).toFixed(2) - parseFloat(item.title).toFixed(2)
                document.getElementById("total").innerHTML = total_price.toFixed(2)
                no_orders()
            }
        })
    })
})


document.querySelector('.purchase').addEventListener("click", function(){

        methods = document.querySelectorAll('[name="payment_method"]')
        for (i = 0; i < methods.length; i++){
            if (methods[i].checked){
                payment_method = methods[i].value
            }
        }
        $.ajax ({
            Type: 'POST',
            url: "/users/set_pre_order/",
            data: {"payment_method": payment_method},
            success: function (response) {
                if (response.error){
                    messageWrap = document.getElementById("messages")
                    if (!messageWrap.hasChildNodes()){
                        message = document.createElement("div")
                        message.innerHTML = response.error
                        messageWrap.appendChild(message)
                    }
                }
                if (response.redirect){
                    window.location.href = "/users/" + response.redirect + "/" + response.order
                }
            }
    })
})


