const searchButton = document.getElementById('searchButton');
const searchInput = document.getElementById('searchInput');
const cartItems = document.getElementById('cartItems');
const cartTotal = document.getElementById('cartTotal');
const addToCartButtons = document.getElementsByClassName('add-to-cart');
const checkoutButton = document.getElementById('checkoutButton');

let cart = [];
let total = 0;

// Dummy product data
const products = [
    { id: 1, name: 'Product 1', price: 19.99 },
    { id: 2, name: 'Product 2', price: 29.99 },
    { id: 3, name: 'Product 3', price: 9.99 },
];

// Render products
function renderProducts() {
    const productList = document.querySelector('.product-list');
    productList.innerHTML = '';

    products.forEach((product) => {
        const productDiv = document.createElement('div');
        productDiv.className = 'product';
        productDiv.innerHTML = `
            <h2>${product.name}</h2>
            <p>Price: $${product.price.toFixed(2)}</p>
            <button class="add-to-cart" data-id="${product.id}">Add to Cart</button>
        `;

        productList.appendChild(productDiv);
    });

    updateCartUI();
}

// Add product to cart
function addToCart(productId) {
    const product = products.find((p) => p.id === productId);
    if (product) {
        cart.push(product);
        total += product.price;
    }
}

// Remove product from cart
function removeFromCart(productId) {
    const productIndex = cart.findIndex((p) => p.id === productId);
    if (productIndex !== -1) {
        const product = cart.splice(productIndex, 1)[0];
        total -= product.price;
    }
}

// Update cart user interface
function updateCartUI() {
    cartItems.innerHTML = '';
    cart.forEach((product) => {
        const cartItem = document.createElement('li');
        cartItem.innerText = `${product.name} - $${product.price.toFixed(2)}`;
        cartItems.appendChild(cartItem);
    });

    cartTotal.innerText = total.toFixed(2);
}

// Handle search button click
searchButton.addEventListener('click', () => {
    const searchTerm = searchInput.value.toLowerCase();
    const filteredProducts = products.filter(
        (product) => product.name.toLowerCase().includes(searchTerm)
    );
    products.length = 0;
    products.push(...filteredProducts);
    renderProducts();
});

// Handle add to cart button click
for (const button of addToCartButtons) {
    button.addEventListener('click', () => {
        const productId = parseInt(button.getAttribute('data-id'));
        addToCart(productId);
        updateCartUI();
    });
}

// Handle checkout button click
checkoutButton.addEventListener('click', () => {
    alert(`Thank you for your purchase!\nTotal: $${total.toFixed(2)}`);
    cart.length = 0;
    total = 0;
    updateCartUI();
});

// Initial render of products
renderProducts();