let slideIndex = 1;
let slideInterval;
let currentPage = 'home';

function showSlides(n) {
  const slidesContainer = document.querySelector('.slider-container');
  if (!slidesContainer) return;

  let i;
  let slides = slidesContainer.getElementsByClassName("mySlides");
  if (!slides || slides.length === 0) return;

  if (n > slides.length) { slideIndex = 1; }
  if (n < 1) { slideIndex = slides.length; }

  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }

  slides[slideIndex - 1].style.display = "block";
}

// Function to navigate to the next or previous slide
function plusSlides(n) {
  stopAutoSlide(); // Stop auto-slide when manually navigating
  showSlides(slideIndex += n);
  // Restart auto-slide after manual navigation
  setTimeout(startAutoSlide, 1000);
}

// Function to start auto-sliding
function startAutoSlide() {
  // Clear any existing interval first
  if (slideInterval) {
    clearInterval(slideInterval);
  }
  slideInterval = setInterval(function () {
    plusSlides(1);
  }, 2000); // Increased to 3 seconds for smoother experience
}

// Function to stop auto-sliding
function stopAutoSlide() {
  if (slideInterval) {
    clearInterval(slideInterval);
    slideInterval = null;
  }
}

// Function to continue shopping after order confirmation
function continueShopping() {
  // Reset cart and details (if using localStorage)
  localStorage.removeItem('cartItems');
  localStorage.removeItem('orderDetails');

  // Redirect to the home page
  window.location.href = '/';
}

// Function to send data for adding items to cart (from index page)
function sendData(button) {
  const form = button.closest('form');
  
  // Check if this is from index page (has .add-to-cart-form class)
  if (form.classList.contains('add-to-cart-form')) {
    // Add to cart functionality
    const productName = form.querySelector('.product-name').value;
    const productPrice = form.querySelector('.product-price-input').value;
    const quantity = form.querySelector('.quantity-input').value;

    console.log("Product Name:", productName);
    console.log("Product Price:", productPrice);
    console.log("Quantity:", quantity);

    // Map to the old parameter names for Django views (for backward compatibility)
    const dataToSend = { 
      productName: productName, 
      productPrice: productPrice, 
      quantity: quantity 
    };
    const url = new URL('/add-to-cart', window.location.origin);
    Object.keys(dataToSend).forEach(key => url.searchParams.append(key, dataToSend[key]));

    fetch(url)
      .then(response => {
        if (response.ok) {
          console.log('Item added to cart successfully');
          window.location.href = '/cart/';
        } else {
          console.error('Error adding item to cart');
        }
      })
      .catch(error => console.error('Error:', error));
  } 
  // Check if this is from cart page (has .update-form class)
  else if (form.classList.contains('update-form')) {
    // Update cart functionality
    const quantity = form.querySelector('.quantity-input').value;
    const productName = form.querySelector('.product-name').value;

    // Map to the old parameter names for Django views (for backward compatibility)
    const dataToSend = { 
      quantity: quantity, 
      productName: productName 
    };
    const url = new URL('/update_pro', window.location.origin);
    Object.keys(dataToSend).forEach(key => url.searchParams.append(key, dataToSend[key]));

    fetch(url)
      .then(response => {
        if (response.ok) {
          console.log('Cart updated successfully');
          window.location.href = '/cart/';
        } else {
          console.error('Error updating cart');
        }
      })
      .catch(error => console.error('Error:', error));
  }
}

// Initial setup - only run once when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  // Initialize slider only once
  showSlides(slideIndex);
  startAutoSlide();

  // Add hover events for slider
  const sliderContainer = document.querySelector('.slider-container');
  if (sliderContainer) {
    sliderContainer.addEventListener('mouseenter', function () {
      stopAutoSlide();
    });
    
    sliderContainer.addEventListener('mouseleave', function () {
      startAutoSlide();
    });
  }
});
