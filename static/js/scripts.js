
document.getElementById('filter-toggle').addEventListener('click', function() {
    const filterOptions = document.getElementById('filter-options');
    filterOptions.style.display = (filterOptions.style.display === 'none' || filterOptions.style.display === '') ? 'block' : 'none';
});


function filterEvents(type) {
    const eventCards = document.querySelectorAll('.event-card');
    eventCards.forEach(card => {
        const cardDate = new Date(card.dataset.date);
        let shouldDisplay = false;

        switch (type) {
            case 'recent':
                
                shouldDisplay = cardDate > new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
                break;
            case 'popular':
                
                shouldDisplay = card.classList.contains('popular');
                break;
            case 'old':
                
                shouldDisplay = cardDate < new Date(Date.now() - 365 * 24 * 60 * 60 * 1000);
                break;
        }

        card.style.display = shouldDisplay ? 'block' : 'none';
    });
}


document.addEventListener('DOMContentLoaded', function() {
    const eventForm = document.getElementById('eventForm');

    if (eventForm) {
        eventForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const eventName = document.getElementById('eventName').value;
            const eventDescription = document.getElementById('eventDescription').value;
            const eventDate = document.getElementById('eventDate').value;
            const eventTime = document.getElementById('eventTime').value;
            const eventImageInput = document.getElementById('eventImage');
            
            let eventImage = '';
            if (eventImageInput.files.length > 0) {
                const file = eventImageInput.files[0];
                const reader = new FileReader();
                reader.onloadend = function () {
                    eventImage = reader.result;
                    saveEvent(eventName, eventDescription, eventDate, eventTime, eventImage);
                };
                reader.readAsDataURL(file);
            } else {
                saveEvent(eventName, eventDescription, eventDate, eventTime, eventImage);
            }
        });
    }

    function saveEvent(name, description, date, time, image) {
        const eventData = {
            name: name,
            description: description,
            date: date,
            time: time,
            image: image,
            likes: 0,        
            views: 0         
        };

        
        let events = JSON.parse(localStorage.getItem('events')) || [];
        events.push(eventData);
        localStorage.setItem('events', JSON.stringify(events));

        
        window.location.href = 'my-events.html';
    }

    
    const eventList = document.getElementById('eventList');
    if (eventList) {
        const events = JSON.parse(localStorage.getItem('events')) || [];
        events.forEach((event, index) => {
            const eventCard = document.createElement('div');
            eventCard.className = 'event-card';
            eventCard.dataset.date = event.date;
            eventCard.innerHTML = `
                <div class="event-image">
                    <img src="${event.image}" alt="${event.name}">
                </div>
                <div class="event-details">
                    <h3>${event.name}</h3>
                    <p>Date: ${event.date}</p>
                    <p>Time: ${event.time}</p>
                    <p>${event.description}</p>
                    <div class="event-interactions">
                        <button class="like-button" data-index="${index}">Like (${event.likes})</button>
                        <span class="views-counter">
                            <img src="images/view-icon.png" alt="View Icon"> <span class="views-count">${event.views}</span>
                        </span>
                    </div>
                </div>
            `;
            eventList.appendChild(eventCard);
        });

        
        document.querySelectorAll('.like-button').forEach(button => {
            button.addEventListener('click', function() {
                const index = this.dataset.index;
                const events = JSON.parse(localStorage.getItem('events'));
                events[index].likes += 1;
                localStorage.setItem('events', JSON.stringify(events));
                this.textContent = `Like (${events[index].likes})`;
            });
        });

        
        document.querySelectorAll('.event-card').forEach(card => {
            card.addEventListener('mouseover', function() {
                const index = Array.from(document.querySelectorAll('.event-card')).indexOf(this);
                const events = JSON.parse(localStorage.getItem('events'));
                if (events[index]) {
                    events[index].views += 1;
                    localStorage.setItem('events', JSON.stringify(events));
                    this.querySelector('.views-count').textContent = events[index].views;
                }
            });
        });
    }
});
const categoryContainer = document.querySelector('.category-container');
let startX;
let currentTranslate = 0;

categoryContainer.addEventListener('touchstart', (event) => {
    startX = event.touches[0].clientX; // Store the starting position
});

categoryContainer.addEventListener('touchmove', (event) => {
    const currentX = event.touches[0].clientX;
    const difference = currentX - startX; // Calculate the distance moved
    currentTranslate = difference; // Update the translation
    categoryContainer.style.transform = `translateX(${currentTranslate}px)`; // Move the container
});

categoryContainer.addEventListener('touchend', () => {
    // Optionally, add logic to snap to the nearest card
    currentTranslate = 0; // Reset translation
    categoryContainer.style.transform = `translateX(0px)`; // Reset position
});

// Profile Page JavaScript

function loadProfileImage(event) {
    const image = document.getElementById('profileImage');
    const file = event.target.files[0];

    if (file) {
        const imageURL = URL.createObjectURL(file);
        image.src = imageURL;
    }
}

// Handle form submission
document.getElementById('profileForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const description = document.getElementById('description').value;
    const phoneNumber = document.getElementById('phoneNumber').value;
    const oldPassword = document.getElementById('oldPassword').value;
    const newPassword = document.getElementById('newPassword').value;

    // Here you can send this data to your server using AJAX or fetch
    console.log({
        firstName,
        lastName,
        description,
        phoneNumber,
        oldPassword,
        newPassword
    });

    alert('Profile updated!');
});

function saveEvent(event) {
    const eventCard = event.target.closest('.event-card');
    const eventDate = eventCard.getAttribute('data-date');
    const eventName = eventCard.querySelector('h3').innerText;
    
    // Example: creating an object to save
    const savedEvent = {
        name: eventName,
        date: eventDate,
    };
    
    // Save to local storage or implement your own save logic
    const savedEvents = JSON.parse(localStorage.getItem('savedEvents')) || [];
    savedEvents.push(savedEvent);
    localStorage.setItem('savedEvents', JSON.stringify(savedEvents));
    
    // Optional feedback
    alert(`Event "${eventName}" has been saved!`);
}


function attendEvent(event) {
    const eventCard = event.target.closest('.event-card');
    const eventName = eventCard.querySelector('h3').innerText;
    const attendanceStatus = eventCard.querySelector('.attendance-status');

    // Update the attendance status
    attendanceStatus.innerText = `You are attending "${eventName}"!`;

    // Optional: You might also want to persist this state
    console.log(`User has confirmed attendance for: ${eventName}`);
}
function likeEvent(event) {
    const likeButton = event.target.closest('.like-button');
    const likeCountElement = likeButton.querySelector('.like-count');
    
    // Parse current like count and increment it
    let currentCount = parseInt(likeCountElement.innerText);
    currentCount++;
    
    // Update the displayed like count
    likeCountElement.innerText = currentCount;

    // Optional: Add logic to persist likes (local storage, server, etc.)
    // For demonstration, you could log the updated count
    console.log(`Event liked! New count: ${currentCount}`);
}







