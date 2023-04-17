function cancel_coupon (first_total){
    document.getElementById("total").innerHTML = first_total
    document.getElementById("coupon").style.display = "inline-block"
    document.getElementById("submit_button").style.display = "flex"
    document.getElementById("cancel_coupon").style.display = "none"
    document.getElementById("used_coupon_id").remove()
}

document.querySelector(".submit_button").addEventListener("click", function() {

    total = document.getElementById("total").innerText
    let entered_coupon = document.getElementById("coupon").value
    $.ajax ({
        Type: 'GET',
        url: "/users/check_coupon",
        data : {
            "entered_coupon": entered_coupon,
            "total": total,
        },
        success: function (response) {
            if (response.coupon){
                if (response.stat == true){
                    if (document.getElementById("error") !== null){
                        document.getElementById("error").remove()
                    }
                    document.getElementById("total").innerHTML = response.total
                    document.getElementById("coupon").style.display = "none"
                    document.getElementById("submit_button").style.display = "none"
                    document.getElementById("cancel_coupon").style.display = "flex"
                    var coupon_used = document.createElement("span");
                    coupon_used.innerHTML = response.coupon.coupon_code + "-" +  response.coupon.percent + "%"
                    coupon_used.setAttribute("class", "coupon_used");
                    coupon_used.setAttribute("title", response.coupon.coupon_code);
                    coupon_used.setAttribute("id", "used_coupon_id");
                    var wrap = document.querySelector(".coupon_wrap")
                    wrap.insertBefore(coupon_used, wrap.lastChild)
                    document.getElementById("cancel_coupon").addEventListener("click", function(){cancel_coupon(total)})
                }
                if (response.stat == "-1"){
                    if (document.getElementById("error") !== null){
                        document.getElementById("error").remove()
                    }
                    var error = document.createElement("span");
                    error.innerHtml = response.coupon
                    error.setAttribute("class", "error");
                    error.setAttribute("id", "error");
                    var wrap = document.querySelector(".coupon_wrap")
                    wrap.insertBefore(error, wrap.lastChild)
                }
                if (response.stat == "-2"){
                    if (document.getElementById("error") !== null){
                        document.getElementById("error").remove()
                    }
                    var error = document.createElement("span");
                    error.innerHTML = response.coupon
                    error.setAttribute("class", "error");
                    error.setAttribute("id", "error");
                    var wrap = document.querySelector(".coupon_wrap")
                    wrap.insertBefore(error, wrap.lastChild)
                }
            }
        }
    })
});

document.getElementById('finish').addEventListener("click", function(){
    new_total = document.getElementById('total').innerHTML
    coupon = ""
    if (document.getElementById('used_coupon_id') !== null){
        coupon = document.getElementById('used_coupon_id').title
    }
    description = ""
    if (document.getElementById('id_description').value !== null){
        description = document.getElementById('id_description').value
    }
    order_id = document.getElementById('order_id').innerHTML
    $.ajax ({
        Type: 'GET',
        url: "/users/complete_order/" + order_id,
        data: {
            "new_total": new_total,
            "description": description,
            "coupon": coupon,
        },
        success: function (response) {
            if (response.pay == "1"){
               window.location.href = response.redirect + "/" + order_id
            }
            if (response.pay == "2"){
               window.location.href = response.redirect
            }
        }
    })
})
