document.addEventListener('DOMContentLoaded', function () {
    console.log("Page loaded");

    // Fade-in effect for service boxes
    const serviceBoxes = document.querySelectorAll('.service-box');
    serviceBoxes.forEach((box, index) => {
        box.style.opacity = 0; // Start invisible
        box.style.transform = 'translateY(20px)'; // Start slightly lower than original position
        setTimeout(() => {
            box.style.transition = 'opacity 0.6s ease, transform 0.6s ease'; // Smooth transition for both opacity and position
            box.style.opacity = 1; // Fade in to full opacity
            box.style.transform = 'translateY(0)'; // Move to original position (no vertical offset)
        }, index * 200); // Apply staggered delay, so each box fades in after the previous one
    });

    // Hover effect for service boxes
    serviceBoxes.forEach(box => {
        box.addEventListener('mouseover', () => {
            box.style.transform = 'scale(1.05)'; // Scale up slightly when hovered
            box.style.transition = 'transform 0.3s ease'; // Smooth transition for scaling effect
        });
        box.addEventListener('mouseout', () => {
            box.style.transform = 'scale(1)'; // Scale back to normal when hover ends
        });
    });

    // Smooth scrolling for navigation links
    const links = document.querySelectorAll('nav ul li a');
    links.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent default anchor behavior
            const targetId = this.getAttribute('href'); // Get the target section ID from the href
            const targetElement = document.querySelector(targetId); // Find the target section
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' }); // Scroll smoothly to the section
            }
        });
    });
});
