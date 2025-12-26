// State
let voyages = [];
let bookings = [];
let clients = [];

// Tab Navigation
function showTab(tabName) {
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('nav button').forEach(btn => btn.classList.remove('active'));
    
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    if (tabName === 'voyages') loadVoyages();
    if (tabName === 'clients') loadClients();
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

// Clients Management
document.getElementById('clientForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const client = {
        name: document.getElementById('clientName').value,
        messenger_psid: document.getElementById('clientPsid').value,
        phone_number: document.getElementById('clientPhone').value || null,
        national_id: document.getElementById('clientNationalId').value || null
    };
    
    const clientId = document.getElementById('clientId').value;
    
    try {
        if (clientId) {
            await api.updateClient(clientId, client);
        } else {
            await api.createClient(client);
        }
        e.target.reset();
        document.getElementById('clientId').value = '';
        loadClients();
    } catch (error) {
        console.error('Error saving client:', error);
        alert('Failed to save client. Check the console for details.');
    }
});

async function loadClients() {
    try {
        clients = await api.getClients();
        renderClients();
    } catch (error) {
        console.error('Error loading clients:', error);
        clients = [];
        renderClients();
    }
}

function renderClients() {
    const tbody = document.querySelector('#clientsTable tbody');
    tbody.innerHTML = clients.map(c => `
        <tr>
            <td>${c.id}</td>
            <td>${c.name || 'N/A'}</td>
            <td>${c.messenger_psid}</td>
            <td>${c.phone_number || 'N/A'}</td>
            <td>${c.national_id || 'N/A'}</td>
            <td>
                <button class="btn-edit" onclick="editClient(${c.id})">Edit</button>
                <button class="btn-delete" onclick="deleteClient(${c.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function editClient(id) {
    const client = clients.find(c => c.id === id);
    if (!client) return;
    
    document.getElementById('clientId').value = client.id;
    document.getElementById('clientName').value = client.name || '';
    document.getElementById('clientPsid').value = client.messenger_psid;
    document.getElementById('clientPhone').value = client.phone_number || '';
    document.getElementById('clientNationalId').value = client.national_id || '';
    
    // Scroll to form
    document.getElementById('clientForm').scrollIntoView({ behavior: 'smooth' });
}

async function deleteClient(id) {
    if (!confirm('Delete this client? This will also delete their bookings and messages.')) return;
    
    try {
        await api.deleteClient(id);
        loadClients();
    } catch (error) {
        console.error('Error deleting client:', error);
        alert('Failed to delete client. Backend may not be running.');
    }
}

// Bookings Management
document.getElementById('bookingForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const booking = {
        client_id: parseInt(document.getElementById('bookingClient').value),
        trip_id: parseInt(document.getElementById('bookingTrip').value),
        passengers_count: parseInt(document.getElementById('bookingPassengers').value),
        contact_phone: document.getElementById('bookingPhone').value || null,
        notes: document.getElementById('bookingNotes').value || null
    };
    
    try {
        await api.createBooking(booking);
        e.target.reset();
        loadBookings();
        alert('Booking created successfully!');
    } catch (error) {
        console.error('Error creating booking:', error);
        alert('Failed to create booking: ' + error.message);
    }
});

async function loadBookings() {
    try {
        bookings = await api.getBookings();
        
        // Also load clients and trips for the dropdowns
        if (!clients.length) {
            clients = await api.getClients();
        }
        if (!voyages.length) {
            voyages = await api.getVoyages();
        }
        
        populateBookingDropdowns();
        renderBookings();
    } catch (error) {
        console.error('Error loading bookings:', error);
        bookings = [];
        renderBookings();
    }
}

function populateBookingDropdowns() {
    // Populate clients dropdown
    const clientSelect = document.getElementById('bookingClient');
    clientSelect.innerHTML = '<option value="">Select Client</option>' +
        clients.map(c => `<option value="${c.id}">${c.name || c.messenger_psid}</option>`).join('');
    
    // Populate trips dropdown
    const tripSelect = document.getElementById('bookingTrip');
    tripSelect.innerHTML = '<option value="">Select Trip</option>' +
        voyages.filter(v => v.is_active).map(v => 
            `<option value="${v.id}">${v.destination} - $${v.price} (${v.available_seats} seats)</option>`
        ).join('');
}

function renderBookings() {
    const tbody = document.querySelector('#bookingsTable tbody');
    tbody.innerHTML = bookings.map(b => {
        // Map IDs to actual client and trip data
        let clientName = 'Unknown';
        if (b.client) {
            // Backend returned full client object
            clientName = b.client.name || b.client.messenger_psid || 'Unknown';
        } else if (b.client_id) {
            // Only have client_id, find in our clients array
            const client = clients.find(c => c.id === b.client_id);
            clientName = client ? (client.name || client.messenger_psid) : `Client #${b.client_id}`;
        }
        
        let tripDest = 'N/A';
        if (b.trip) {
            // Backend returned full trip object
            tripDest = b.trip.destination;
        } else if (b.trip_id) {
            // Only have trip_id, find in our voyages array
            const trip = voyages.find(v => v.id === b.trip_id);
            tripDest = trip ? trip.destination : `Trip #${b.trip_id}`;
        }
        
        const bookingDate = b.created_at ? new Date(b.created_at).toLocaleDateString() : 'N/A';
        const passengers = b.passengers_count || 1;
        const phone = b.contact_phone || 'N/A';
        
        return `
        <tr>
            <td>${b.id}</td>
            <td>${clientName}</td>
            <td>${tripDest}</td>
            <td>${passengers}</td>
            <td>${phone}</td>
            <td><span class="status-${b.status}">${b.status}</span></td>
            <td>${bookingDate}</td>
            <td>
                ${b.status === 'pending' ? 
                    `<button class="btn-confirm" onclick="confirmBooking(${b.id})">Confirm</button>` : 
                    ''}
                ${b.status !== 'cancelled' ? 
                    `<button class="btn-cancel" onclick="cancelBooking(${b.id})">Cancel</button>` : 
                    ''}
            </td>
        </tr>
        `;
    }).join('');
}

async function confirmBooking(id) {
    if (!confirm('Confirm this booking?')) return;
    
    try {
        await api.confirmBooking(id);
        loadBookings();
    } catch (error) {
        console.error('Error confirming booking:', error);
        alert('Failed to confirm booking: ' + error.message);
    }
}

async function cancelBooking(id) {
    if (!confirm('Cancel this booking?')) return;
    
    try {
        await api.cancelBooking(id);
        loadBookings();
    } catch (error) {
        console.error('Error cancelling booking:', error);
        alert('Failed to cancel booking: ' + error.message);
    }
}

// Analytics
async function loadAnalytics() {
    try {
        // Load bookings and voyages first if not already loaded
        if (!bookings.length) {
            bookings = await api.getBookings();
        }
        if (!voyages.length) {
            voyages = await api.getVoyages();
        }
        
        const analytics = await api.getAnalytics();
        updateAnalyticsDisplay(analytics);
    } catch (error) {
        console.error('Error loading analytics:', error);
        updateAnalyticsDisplay({
            total_bookings: 0,
            active_voyages: 0,
            total_revenue: 0,
            total_conversations: 0
        });
    }
}

function updateAnalyticsDisplay(data) {
    document.getElementById('totalBookings').textContent = data.total_bookings || 0;
    document.getElementById('activeVoyages').textContent = data.active_voyages || 0;
    document.getElementById('totalRevenue').textContent = `$${(data.total_revenue || 0).toLocaleString()}`;
    document.getElementById('totalConversations').textContent = data.total_conversations || 0;
    
    // Draw bookings and revenue charts with real data
    drawBookingsChart();
    drawRevenueChart();
}

function drawBookingsChart() {
    const canvas = document.getElementById('bookingsChart');
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = 200;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Get bookings data grouped by date (last 7 days)
    const last7Days = [];
    const bookingCounts = [];
    const today = new Date();
    
    for (let i = 6; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        last7Days.push(dateStr);
        
        // Count bookings for this date
        const count = bookings.filter(b => {
            if (!b.created_at) return false;
            const bookingDate = new Date(b.created_at);
            return bookingDate.toDateString() === date.toDateString();
        }).length;
        
        bookingCounts.push(count);
    }
    
    // Draw chart
    if (bookingCounts.length === 0 || bookingCounts.every(c => c === 0)) {
        // No data - show message
        ctx.fillStyle = '#999';
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('No booking data available', canvas.width / 2, canvas.height / 2);
        return;
    }
    
    const maxValue = Math.max(...bookingCounts, 1);
    const barWidth = canvas.width / bookingCounts.length;
    const padding = 40;
    const chartHeight = canvas.height - padding;
    
    ctx.fillStyle = '#007bff';
    bookingCounts.forEach((value, i) => {
        const barHeight = (value / maxValue) * chartHeight * 0.8;
        const x = i * barWidth + 10;
        const y = chartHeight - barHeight;
        
        // Draw bar
        ctx.fillRect(x, y, barWidth - 20, barHeight);
        
        // Draw value on top of bar
        ctx.fillStyle = '#333';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(value, x + (barWidth - 20) / 2, y - 5);
        
        // Draw date label
        ctx.fillStyle = '#666';
        ctx.font = '10px Arial';
        ctx.fillText(last7Days[i], x + (barWidth - 20) / 2, canvas.height - 5);
        
        ctx.fillStyle = '#007bff';
    });
}

function drawRevenueChart() {
    const canvas = document.getElementById('revenueChart');
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = 200;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Get revenue data grouped by date (last 7 days)
    const last7Days = [];
    const revenueByDay = [];
    const today = new Date();
    
    for (let i = 6; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        last7Days.push(dateStr);
        
        // Calculate revenue for this date
        const dayRevenue = bookings
            .filter(b => {
                if (!b.created_at || b.status !== 'confirmed') return false;
                const bookingDate = new Date(b.created_at);
                return bookingDate.toDateString() === date.toDateString();
            })
            .reduce((sum, b) => {
                // Find the trip to get price
                const trip = voyages.find(v => v.id === b.trip_id);
                const tripPrice = trip?.price || 0;
                const passengers = b.passengers_count || 1;
                return sum + (tripPrice * passengers);
            }, 0);
        
        revenueByDay.push(dayRevenue);
    }
    
    // Draw chart
    if (revenueByDay.length === 0 || revenueByDay.every(r => r === 0)) {
        // No data - show message
        ctx.fillStyle = '#999';
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('No revenue data available', canvas.width / 2, canvas.height / 2);
        return;
    }
    
    const maxValue = Math.max(...revenueByDay, 1);
    const barWidth = canvas.width / revenueByDay.length;
    const padding = 40;
    const chartHeight = canvas.height - padding;
    
    ctx.fillStyle = '#28a745';
    revenueByDay.forEach((value, i) => {
        const barHeight = (value / maxValue) * chartHeight * 0.8;
        const x = i * barWidth + 10;
        const y = chartHeight - barHeight;
        
        // Draw bar
        ctx.fillRect(x, y, barWidth - 20, barHeight);
        
        // Draw value on top of bar
        ctx.fillStyle = '#333';
        ctx.font = '11px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`$${value.toLocaleString()}`, x + (barWidth - 20) / 2, y - 5);
        
        // Draw date label
        ctx.fillStyle = '#666';
        ctx.font = '10px Arial';
        ctx.fillText(last7Days[i], x + (barWidth - 20) / 2, canvas.height - 5);
        
        ctx.fillStyle = '#28a745';
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
