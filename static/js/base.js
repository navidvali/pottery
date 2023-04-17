const open = document.getElementById("open_menu")
const close = document.getElementById("close_menu")
const wrap = document.getElementById("wrap_nav_button")

open.addEventListener("click", ()=>{
    wrap.style.display = "grid";
    open.style.display = "none";
    close.style.display = "block";
})

close.addEventListener("click", ()=>{
    wrap.style.display = "none";
    open.style.display = "block";
    close.style.display = "none";
})