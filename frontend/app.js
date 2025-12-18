// State
let voyages = [];
let bookings = [];

// Tab Navigation
function showTab(tabName) {
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('nav button').forEach(btn => btn.classList.remove('active'));
    
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    if (tabName === 'voyages') loadVoyages();
    if (tabName === 'bookings') loadBookings();
    if (tabName === 'analytics') loadAnalytics();
}

// Bot Toggle
document.getElementById('botEnabled').addEventListener('change', async (e) => {
    try {
        await api.setBotStatus(e.target.checked);
        alert(`Chatbot ${e.target.checked ? 'enabled' : 'disabled'}`);
    } catch (error) {
        console.error('Error updating bot status:', error);
        e.target.checked = !e.target.checked;
        alert('Failed to update bot status. Backend may not be running.');
    }
});

// Voyages Management
document.getElementById('voyageForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const voyage = {
        destination: document.getElementById('destination').value,
        start_date: document.getElementById('startDate').value,
        end_date: document.getElementById('endDate').value,
        price: parseFloat(document.getElementById('price').value),
        capacity: parseInt(document.getElementById('capacity').value)
    };
    
    const voyageId = document.getElementById('voyageId').value;
    
    try {
        if (voyageId) {
            await api.updateVoyage(voyageId, voyage);
        } else {
            await api.createVoyage(voyage);
        }
        e.target.reset();
        loadVoyages();
    } catch (error) {
        console.error('Error saving voyage:', error);
        alert('Failed to save voyage. Backend may not be running.');
    }
});

async function loadVoyages() {
    try {
        voyages = await api.getVoyages();
        renderVoyages();
    } catch (error) {
        console.error('Error loading voyages:', error);
        // Show mock data if backend is not available
        voyages = [
            { id: 1, destination: 'Paris', start_date: '2025-06-01', end_date: '2025-06-07', price: 1200, capacity: 30 },
            { id: 2, destination: 'Tokyo', start_date: '2025-07-15', end_date: '2025-07-25', price: 2500, capacity: 20 }
        ];
        renderVoyages();
    }
}

function renderVoyages() {
    const tbody = document.querySelector('#voyagesTable tbody');
    tbody.innerHTML = voyages.map(v => {
        // Handle both frontend format and backend format
        const startDate = v.start_date || (v.departure_time ? v.departure_time.split('T')[0] : '');
        const endDate = v.end_date || (v.arrival_time ? v.arrival_time.split('T')[0] : '');
        const capacity = v.capacity || v.available_seats || 0;
        
        return `
        <tr>
            <td>${v.id}</td>
            <td>${v.destination}</td>
            <td>${startDate}</td>
            <td>${endDate}</td>
            <td>$${v.price || 0}</td>
            <td>${capacity}</td>
            <td>
                <button class="btn-edit" onclick="editVoyage(${v.id})">Edit</button>
                <button class="btn-delete" onclick="deleteVoyage(${v.id})">Delete</button>
            </td>
        </tr>
        `;
    }).join('');
}

function editVoyage(id) {
    const voyage = voyages.find(v => v.id === id);
    if (!voyage) return;
    
    document.getElementById('voyageId').value = voyage.id;
    document.getElementById('destination').value = voyage.destination;
    
    // Handle both frontend and backend date formats
    const startDate = voyage.start_date || (voyage.departure_time ? voyage.departure_time.split('T')[0] : '');
    const endDate = voyage.end_date || (voyage.arrival_time ? voyage.arrival_time.split('T')[0] : '');
    
    document.getElementById('startDate').value = startDate;
    document.getElementById('endDate').value = endDate;
    document.getElementById('price').value = voyage.price || 0;
    document.getElementById('capacity').value = voyage.capacity || voyage.available_seats || 0;
}

async function deleteVoyage(id) {
    if (!confirm('Delete this voyage?')) return;
    
    try {
        await api.deleteVoyage(id);
        loadVoyages();
    } catch (error) {
        console.error('Error deleting voyage:', error);
        alert('Failed to delete voyage. Backend may not be running.');
    }
}

// Bookings Management
async function loadBookings() {
    try {
        bookings = await api.getBookings();
        renderBookings();
    } catch (error) {
        console.error('Error loading bookings:', error);
        // Show mock data if backend is not available
        bookings = [
            { id: 1, client: 'John Doe', voyage: 'Paris', date: '2025-06-01', status: 'confirmed' },
            { id: 2, client: 'Jane Smith', voyage: 'Tokyo', date: '2025-07-15', status: 'pending' }
        ];
        renderBookings();
    }
}

function renderBookings() {
    const tbody = document.querySelector('#bookingsTable tbody');
    tbody.innerHTML = bookings.map(b => {
        // Handle backend data structure
        const clientName = b.client?.name || b.client || 'Unknown';
        const tripDest = b.trip?.destination || b.voyage || 'N/A';
        const bookingDate = b.date || (b.created_at ? new Date(b.created_at).toLocaleDateString() : 'N/A');
        
        return `
        <tr>
            <td>${b.id}</td>
            <td>${clientName}</td>
            <td>${tripDest}</td>
            <td>${bookingDate}</td>
            <td>${b.status}</td>
            <td>
                ${b.status !== 'cancelled' ? 
                    `<button class="btn-cancel" onclick="cancelBooking(${b.id})">Cancel</button>` : 
                    '<span>-</span>'
                }
            </td>
        </tr>
        `;
    }).join('');
}

async function cancelBooking(id) {
    if (!confirm('Cancel this booking?')) return;
    
    try {
        await api.cancelBooking(id);
        loadBookings();
    } catch (error) {
        console.error('Error cancelling booking:', error);
        alert('Failed to cancel booking. Backend may not be running.');
    }
}

// Analytics
async function loadAnalytics() {
    try {
        const analytics = await api.getAnalytics();
        updateAnalyticsDisplay(analytics);
    } catch (error) {
        console.error('Error loading analytics:', error);
        // Show mock data if backend is not available
        const mockAnalytics = {
            total_bookings: 127,
            active_voyages: 8,
            total_revenue: 45600,
            total_conversations: 342
        };
        updateAnalyticsDisplay(mockAnalytics);
    }
}

function updateAnalyticsDisplay(data) {
    document.getElementById('totalBookings').textContent = data.total_bookings || 0;
    document.getElementById('activeVoyages').textContent = data.active_voyages || 0;
    document.getElementById('totalRevenue').textContent = `$${(data.total_revenue || 0).toLocaleString()}`;
    document.getElementById('totalConversations').textContent = data.total_conversations || 0;
    
    // Simple chart (using HTML/CSS bars)
    const canvas = document.getElementById('bookingsChart');
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = 200;
    
    // Draw simple bar chart
    ctx.fillStyle = '#007bff';
    const mockData = [10, 15, 12, 18, 22, 30, 28];
    const barWidth = canvas.width / mockData.length;
    const maxValue = Math.max(...mockData);
    
    mockData.forEach((value, i) => {
        const barHeight = (value / maxValue) * canvas.height * 0.8;
        ctx.fillRect(i * barWidth + 5, canvas.height - barHeight, barWidth - 10, barHeight);
    });
}

// Admin Chatbot
document.getElementById('chatForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const input = document.getElementById('chatInput');
    const message = input.value;
    
    addChatMessage(message, 'user');
    input.value = '';
    
    try {
        const response = await api.sendAdminMessage(message);
        addChatMessage(response.reply, 'bot');
    } catch (error) {
        console.error('Error sending message:', error);
        addChatMessage('Sorry, the backend is not available. Please check the server connection.', 'bot');
    }
});

function addChatMessage(text, sender) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = text;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Initialize
loadVoyages();
