var shoppingCart = (function() {
    cart = [];

    // Constructor
    function Item(id, name, price, quantity, size) {
        this.id = id;
        this.name = name;
        this.price = price;
        this.quantity = quantity;
        this.size = size;
    }

    // Save cart
    function saveCart() {
        localStorage.setItem('order', JSON.stringify(cart));
    }

    // Load cart
    function loadCart() {
        cart = JSON.parse(localStorage.getItem('order'));
    }
    if (localStorage.getItem('order') != null) {
        loadCart();
    }


    var obj = {};

    // Add to cart
    obj.addItemToCart = function(id, size) {
        for(var item in cart) {
            if(cart[item].id === id && cart[item].size === size) {
                cart[item].quantity ++;
                saveCart();
                return;
            }
        }
        var item = new Item(id, name, price, quantity, size);
        cart.push(item);
        saveCart();
    }


    // Remove item from cart
    obj.removeItemFromCart = function(id, size) {
        for(var item in cart) {
            if(cart[item].id === id && cart[item].size === size) {
                cart[item].quantity --;
                if(cart[item].quantity <= 1) {
                    cart[item].quantity = 1;
                }
                break;
            }
        }
        saveCart();
    }

    // Remove all items from cart
    obj.removeItemFromCartAll = function(id, size) {
        for(var item in cart) {
            if(cart[item].id === id && cart[item].size === size) {
                cart.splice(item, 1);
                break;
            }
        }
        saveCart();
    }

    // Clear cart
    obj.clearCart = function() {
        cart = [];
        saveCart();
    }

    // Count cart
    obj.totalCount = function() {
        var totalCount = 0;
        for(var item in cart) {
            totalCount += cart[item].quantity;
        }
        return totalCount;
    }

    // Total cart
    obj.totalCart = function() {
        var totalCart = 0;
        for(var item in cart) {

            totalCart += cart[item].price * cart[item].quantity;
        }
        return Number(totalCart.toFixed(2));
    }

    // List cart
    obj.listCart = function() {
        var cartCopy = [];
        for(i in cart) {
            item = cart[i];
            itemCopy = {};
            for(p in item) {
                itemCopy[p] = item[p];

            }
            itemCopy.total = Number(item.price * item.quantity).toFixed(2);
            cartCopy.push(itemCopy)
        }
        return cartCopy;
    }

    return obj;
})();

function displayCart() {
    var cartArray = shoppingCart.listCart();
    var output = "";
    for(var i in cartArray) {
        let sizeDisplayname = '';

            if (cartArray[i].size === 'small'){
             sizeDisplayname = 'Фуршетные';
            } else if (cartArray[i].size === 'large') {
                sizeDisplayname = 'Большие';
            } else {
                sizeDisplayname = '';
            }

        output += "<tr class='cart-row'>"
            + "<td class='align-middle'><div class=\"small-Img\"><img src=" + cartArray[i].image + "></div></td>"
            + "<td><div class='text-al-justif mt-3'><h5>" + cartArray[i].name + "</h5><p class='font-italic text-black-50'>" + sizeDisplayname + "</p></div></td>"
            + "<td class='align-middle'>" + cartArray[i].price + "</td>"
            + "<td class='align-middle'><div class='input-group mr-3'><span class='minus-item font-weight-bold'" +
            " data-id=" + cartArray[i].id + " data-size=" + cart[i].size + ">-</span>"
            + "<span type='number' " +
            "class='item-count font-weight-bold' data-id='" + cartArray[i].id + "'>" + cartArray[i].quantity + "</span>"
            + "<span " +
            "class='plus-item font-weight-bold' data-id=" + cartArray[i].id + "" +
            " data-size=" + cartArray[i].size + ">+</span></div></td>"
            + "<td class='align-middle font-weight-bold for-font_sht'>" + cartArray[i].total + "</td>"
            + "<td class='align-middle'><button class='delete-item' data-id=" + cartArray[i].id + "" +
            " data-size=" + cart[i].size + ">X</button></td>"
            +  "</tr>"
        ;
    }
    $('.show-cart').html(output);
    $('.total-cart').html(shoppingCart.totalCart());
    $('.total-count').html(shoppingCart.totalCount());

}

// Delete item button

$('.show-cart').on("click", ".delete-item", function(event) {
    var id = $(this).data('id');
    var size = $(this).data('size');
    shoppingCart.removeItemFromCartAll(id, size);
    displayCart();
})


// -1
$('.show-cart').on("click", ".minus-item", function(event) {
    var id = $(this).data('id');
    var size = $(this).data('size');
    shoppingCart.removeItemFromCart(id, size);
    displayCart();
})
// +1
$('.show-cart').on("click", ".plus-item", function(event) {
    var id = $(this).data('id');
    var size = $(this).data('size');
    shoppingCart.addItemToCart(id, size);
    displayCart();
})

displayCart();

$(".confirm-order").click(function() {
    var totalPrice = shoppingCart.totalCart();
        if (totalPrice <= 20) {
            document.getElementById("alert-message").style.display = 'block';
        } else {
            localStorage.setItem('total', totalPrice.toFixed(2));
            window.location="/order"
        }

});
