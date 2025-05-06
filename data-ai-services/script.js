// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Form submission handling
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(this);
        const data = Object.fromEntries(formData);
        
        // Here you would typically send the data to your server
        console.log('Form submitted:', data);
        
        // Show success message
        alert('Merci pour votre message ! Nous vous contacterons bientôt.');
        this.reset();
    });
}

// Add animation on scroll
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.service-card, .pricing-card');
    
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementBottom = element.getBoundingClientRect().bottom;
        
        if (elementTop < window.innerHeight && elementBottom > 0) {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }
    });
};

// Set initial styles for animation
document.querySelectorAll('.service-card, .pricing-card').forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'opacity 0.5s, transform 0.5s';
});

// Add scroll event listener
window.addEventListener('scroll', animateOnScroll);

// Trigger initial animation check
animateOnScroll();

// Mobile menu toggle (to be implemented if needed)
const mobileMenuToggle = () => {
    // Add mobile menu functionality here if needed
    console.log('Mobile menu toggle clicked');
};

// Chatbot
const chatbotButton = document.getElementById('chatbot-button');
const chatbotWindow = document.getElementById('chatbot-window');
const chatbotClose = document.getElementById('chatbot-close');
const chatbotForm = document.getElementById('chatbot-form');
const chatbotInput = document.getElementById('chatbot-input');
const chatbotMessages = document.getElementById('chatbot-messages');

const MISTRAL_API_KEY = 'b2zJp2qjtNWemulGz9COD5nAdDawxc5l';
const MISTRAL_API_URL = 'https://api.mistral.ai/v1/chat/completions';

if (chatbotButton && chatbotWindow && chatbotClose && chatbotForm && chatbotInput && chatbotMessages) {
    chatbotButton.onclick = () => {
        chatbotWindow.style.display = 'flex';
        chatbotButton.style.display = 'none';
    };
    chatbotClose.onclick = () => {
        chatbotWindow.style.display = 'none';
        chatbotButton.style.display = 'flex';
    };
    chatbotForm.onsubmit = async (e) => {
        e.preventDefault();
        const userMsg = chatbotInput.value.trim();
        if (!userMsg) return;
        addChatMessage(userMsg, 'user');
        chatbotInput.value = '';
        addChatMessage('...', 'bot');
        const botReply = await getMistralReply(userMsg);
        // Remplace le dernier message '...' par la vraie réponse
        const allMsgs = chatbotMessages.querySelectorAll('.chatbot-message.bot');
        allMsgs[allMsgs.length-1].textContent = botReply;
    };
}

function addChatMessage(text, sender) {
    const msg = document.createElement('div');
    msg.className = 'chatbot-message ' + sender;
    msg.textContent = text;
    chatbotMessages.appendChild(msg);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

async function getMistralReply(userMsg) {
    try {
        const response = await fetch(MISTRAL_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + MISTRAL_API_KEY
            },
            body: JSON.stringify({
                model: 'mistral-tiny',
                messages: [
                    { role: 'system', content: "Tu es le chatbot Datafish. Sois chaleureux et professionnel. Datafish est une entreprise experte en data science et intelligence artificielle, accompagnant les entreprises dans la valorisation de leurs données, l'automatisation, l'analyse avancée et la transformation digitale. Nous proposons des prestations simples, raisonnables, facturées à l'heure avec une transparence totale sur les tarifs et la mission. La relation client est basée sur la clarté et la confiance. Ce site internet et ce chatbot ont été développés par Datafish. Propose toujours un rendez-vous téléphonique, précise que le devis est gratuit, et invite à laisser un numéro de téléphone pour être rappelé par un expert Datafish." },
                    { role: 'user', content: userMsg }
                ]
            })
        });
        if (!response.ok) return "Désolé, une erreur est survenue.";
        const data = await response.json();
        return data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content
            ? data.choices[0].message.content.trim()
            : "Désolé, je n'ai pas compris.";
    } catch (e) {
        return "Désolé, je n'arrive pas à joindre le service IA.";
    }
} 