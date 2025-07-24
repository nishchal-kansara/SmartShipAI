// Initialize distance slider
function syncDistance(value) {
    document.getElementById("distanceValue").innerText = value + " km";
    document.getElementById("distanceInput").value = value;
}

function syncDistanceInput(value) {
    const slider = document.getElementById("distance");
    if (value >= 5 && value <= 1000) {
        slider.value = value;
        document.getElementById("distanceValue").innerText = value + " km";
    }
}

// Animation on scroll
document.addEventListener('DOMContentLoaded', function () {
    const animateElements = document.querySelectorAll('.animate-up');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    animateElements.forEach(element => {
        observer.observe(element);
    });

    // Smooth scrolling for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Navbar scroll effect
window.addEventListener('scroll', function () {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.padding = '10px 0';
        navbar.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.4)';
    } else {
        navbar.style.padding = '15px 0';
        navbar.style.boxShadow = 'none';
    }
});

const form = document.getElementById('contactForm');
const statusMessage = document.getElementById('statusMessage');
const statusContainer = document.getElementById('statusContainer');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    try {
        const response = await fetch('https://flask-mail-ft2p.onrender.com/submit', {
            method: 'POST',
            body: formData
        });

        statusContainer.style.display = 'block'; // Show container

        if (response.ok) {
            statusContainer.className = 'alert alert-success';
            statusMessage.textContent = "Your message has been sent successfully!";
            form.reset();
        } else {
            statusContainer.className = 'alert alert-danger';
            statusMessage.textContent = "Oops! Something went wrong.";
        }
    } catch (error) {
        statusContainer.style.display = 'block';
        statusContainer.className = 'alert alert-danger';
        statusMessage.textContent = "An error occurred. Please try again.";
    }
});
