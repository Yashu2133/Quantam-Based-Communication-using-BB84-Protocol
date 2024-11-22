document.addEventListener("DOMContentLoaded", function() {
    const contactForm = document.getElementById("contactForm");
    contactForm.addEventListener("submit", function(event) {
        event.preventDefault();
        
        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const message = document.getElementById("message").value;

        // Handle form submission here
        // For example, send data to a server or display a thank you message
        console.log("Name:", name, "Email:", email, "Message:", message);

        alert("Thank you for your message, " + name + "!");
    });

    // Additional JavaScript functionality can be added here
});
