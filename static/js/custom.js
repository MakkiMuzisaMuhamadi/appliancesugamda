$(document).ready(function () {
    // Handle category button click
    $('.tablinks').on('click', function () {
        var categoryId = $(this).data('category-id');

        // Hide all products
        $('.brandcontent').hide();

        // Show products related to the selected category
        if (categoryId === undefined) {
            $('.brandcontent').show(); // Show all products if "All" is selected
        } else {
            // Show products related to the selected category
            $('.brandcontent[data-product-category-id="' + categoryId + '"]').show();
        }

        // Hide brands not related to the selected category
        $('.brand').hide();
        $('.brand[data-brand-category-id="' + categoryId + '"]').show();
    });

    // Handle brand button click
    $('.brand').on('click', function () {
        var brandCategoryId = $(this).data('brand-category-id');

        // Hide all products
        $('.brandcontent').hide();

        // Show products related to the selected brand category
        if (brandCategoryId === 'all') {
            $('.brandcontent').show(); // Show all products if "All" is selected
        } else {
            // Show products related to the selected brand category
            $('.brandcontent[data-product-brand-id="' + brandCategoryId + '"]').show();
        }
    });

    // Fade out loader and fade in content after 2 seconds
    setTimeout(function () {
        $('.fh5co-loader').fadeOut();
        $('.container-fluid').fadeIn();
    }, 2000);

    // Set up automatic slideshow
    var slides = document.querySelectorAll('.responsive-image img');
    var currentSlide = 0;
    var slideInterval = setInterval(nextSlide, 6000);

    function nextSlide() {
        slides[currentSlide].classList.remove('active');
        currentSlide = (currentSlide + 1) % slides.length;
        slides[currentSlide].classList.add('active');
    }

    // Function to update cart count
    function updateCartCount() {
        fetch("{% url 'get_cart_count' %}")
            .then(response => response.json())
            .then(data => {
                // Update cart count in the DOM
                document.getElementById('cart-count').innerText = data.count;
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Call the function initially to set the cart count
    updateCartCount();

    // Handle add to cart button click
    var addToCartButtons = document.querySelectorAll('.add-to-cart-btn button');
    addToCartButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            var productId = this.getAttribute('data-product-id');
            addToCart(productId);
        });
    });

    // Function to add product to cart
    function addToCart(productId) {
        fetch("{% url 'add_to_cart' 0 %}".replace('0', productId), {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        })   
        .then(response => response.json())
        .then(data => {
            // Display the flash message
            showToast(data.message, data.status, 100000);
            updateCartCount(); // Update cart count after adding to cart
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Function to display toast message
    function showToast(message, status, duration) {
        let box = document.createElement("div");
        box.classList.add("toast", `toast-${status}`);
        box.innerHTML = `<div class="toast-content-wrapper">
                        <div class="toast-message">${message}</div>
                        <div class="toast-progress"></div>
                    </div>`;
        duration = duration || 5000;
        box.querySelector(".toast-progress").style.animationDuration =
            `${duration / 1000}s`;

        let toastAlready =
            document.body.querySelector(".toast");
        if (toastAlready) {
            toastAlready.remove();
        }

        document.body.appendChild(box);
    }

    // Handle custom toast click
    let submit = document.querySelector(".custom-toast");
    submit.addEventListener("click", (e) => {
        showToast("Article Submitted Successfully", "success", 100000);
    });

    // Handle warning click
    warn.addEventListener("click", (e) => {
        e.preventDefault();
        showToast("!warning! server error", "warning", 5000);
    });

    // Hide message container after 3 seconds
    setTimeout(function () {
        document.getElementById('message-container').style.display = 'none';
    }, 3000);
});
