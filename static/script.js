// Navigate to security check
function navigateToHome() {
    window.location.href = "/home";
}

// Smooth scroll to "How It Works" section
function scrollToHowItWorks() {
    const howItWorksSection = document.querySelector('.how-it-works');
    if (howItWorksSection) {
        howItWorksSection.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }
}

