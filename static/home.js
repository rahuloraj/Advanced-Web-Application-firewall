document.getElementById("submit-btn").addEventListener("click", function () {
    let userInput = document.getElementById("user-input").value;
    let resultDiv = document.getElementById("result");

    // Show loading animation
    document.getElementById("loading").style.display = "block";
    resultDiv.innerHTML = "";

    fetch("/check_request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_request: userInput })
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading animation
        document.getElementById("loading").style.display = "none";

        // Enhanced result display with animations
        if (data.status === "malicious") {
            resultDiv.innerHTML = `
                <div class="result-box danger">
                    <div class="result-icon">🚨</div>
                    <div class="result-message">
                        <div class="pulse-text">${data.message}</div>
                        <div class="sub-text">Our security system has detected and blocked this malicious request.</div>
                    </div>
                </div>
            `;
        } 
        else if (data.status === "obfuscated") {
            resultDiv.innerHTML = `
                <div class="result-box warning">
                    <div class="result-icon">🔍</div>
                    <div class="result-message">
                        <div class="pulse-text">${data.message}</div>
                        <div class="ai-verdict">${data.ml_verdict}</div>
                        <div class="sub-text">AI-powered deep analysis complete.</div>
                    </div>
                </div>
            `;
        } 
        else {
            resultDiv.innerHTML = `
                <div class="result-box success">
                    <div class="result-icon">✅</div>
                    <div class="result-message">
                        <div class="pulse-text">${data.message}</div>
                        <div class="sub-text">Your request has been verified and cleared by our security system.</div>
                    </div>
                </div>
            `;
        }

        // Add animation class
        resultDiv.querySelector('.result-box').classList.add('fade-in');
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("loading").style.display = "none";
        resultDiv.innerHTML = `
            <div class="result-box error">
                <div class="result-icon">⚠️</div>
                <div class="result-message">
                    <div class="pulse-text">System Error</div>
                    <div class="sub-text">Unable to process your request. Please try again.</div>
                </div>
            </div>
        `;
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const prevButton = document.querySelector(".tip-nav-btn.prev");
    const nextButton = document.querySelector(".tip-nav-btn.next");
    const slides = document.querySelectorAll(".tip-slide");
    let currentIndex = 0;

    function changeSlide() {
        slides.forEach((slide, index) => {
            slide.classList.remove("active");
            if (index === currentIndex) {
                slide.classList.add("active");
            }
        });
    }

    prevButton.addEventListener("click", () => {
        currentIndex = (currentIndex === 0) ? slides.length - 1 : currentIndex - 1;
        changeSlide();
    });

    nextButton.addEventListener("click", () => {
        currentIndex = (currentIndex === slides.length - 1) ? 0 : currentIndex + 1;
        changeSlide();
    });

    // Initial slide display
    changeSlide();
});

// Add this CSS to your styles
const styles = `
.result-box {
    padding: 1.5rem;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    animation: slideIn 0.3s ease-out;
}

.result-box.danger {
    background: rgba(255, 0, 0, 0.1);
    border: 1px solid rgba(255, 0, 0, 0.2);
}

.result-box.warning {
    background: rgba(222, 49, 99, 0.1); /* Cherry red background */
    border: 1px solid rgba(222, 49, 99, 0.5);
    animation: pulseGlow 1.8s ease-in-out infinite;
    box-shadow: 0 0 10px rgba(222, 49, 99, 0.3);
}

@keyframes pulseGlow {
    0%, 100% {
        transform: scale(1);
        box-shadow: 0 0 10px rgba(222, 49, 99, 0.3);
    }
    50% {
        transform: scale(1.03);
        box-shadow: 0 0 20px rgba(222, 49, 99, 0.5);
    }
}

.result-box.success {
    background: rgba(0, 255, 0, 0.1);
    border: 1px solid rgba(0, 255, 0, 0.2);
}

.result-icon {
    font-size: 2.5rem;
    animation: pulseIcon 2s infinite;
}

.result-message {
    flex: 1;
}

.pulse-text {
    font-size: 1.2rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
    animation: pulseText 2s infinite;
}

.sub-text {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
}

.ai-verdict {
    font-size: 1.1rem;
    margin: 0.5rem 0;
    font-weight: 500;
    color: #00FFD1;
}

@keyframes slideIn {
    from {
        transform: translateY(-10px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

@keyframes pulseIcon {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

@keyframes pulseText {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
}

.fade-in {
    animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
`;

// Add styles to document
const styleSheet = document.createElement("style");
styleSheet.textContent = styles;
document.head.appendChild(styleSheet);
