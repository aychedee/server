var IntThis = {};

document.addEventListener("click", function(e) { 
    if (e.target.id === "register-text") {
        IntThis.hide(document.querySelector("#authenticate"));
        IntThis.show(document.querySelector("div#register"));
        e.preventDefault();
        
    }
    else if (e.target.id === "logout-text") {
        IntThis.hide(document.querySelector("#logout"));
        IntThis.show(document.querySelector("#authenticate"));
        console.log(document.cookie)
        e.preventDefault();
    }
    else if (e.target.id === "signin-text") {
        IntThis.hide(document.querySelector("#signin"));
        IntThis.show(document.querySelector("#authenticate"));
        console.log(document.cookie)
        e.preventDefault();
    }
});

IntThis.hide = function (el) {
    el.className = el.className.replace(/(?:^|\s)dialog(?!\S)/g, "");
    el.setAttribute("style", "display: none");
    return el;
}

IntThis.show = function (el) {
    el.className += " dialog";
    el.setAttribute("style", "display: block");
    return el;
}

IntThis.toggleDisplayed = function (el) {
    if (el.getAttribute("style").indexOf("display: none") === -1) {
        IntThis.hide(el);
    }
    else {
        IntThis.show(el);
    }
    return el;
}

IntThis.addLabelClass = function(el) {
    el.parentNode.setAttribute("alt", el.getAttribute("alt"));
    el.parentNode.setAttribute("title", el.getAttribute("title"));
    el.parentNode.classList.add('label');
}

var increment = 0;
window.onscroll = function () {
    if (document.body.scrollTop + window.innerHeight > document.height - 200) {
        var original = document.querySelector("footer");
        var clone = original.cloneNode(true);
        clone.id = "endless" + ++increment;
        original.parentNode.appendChild(clone);
    }
}
