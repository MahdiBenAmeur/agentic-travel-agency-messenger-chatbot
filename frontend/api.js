// API Configuration
const API_BASE = 'http://localhost:8000/api';

// API Service
const api = {
    // Voyages
    async getVoyages() {
        const response = await fetch(`${API_BASE}/voyages`);
        return response.json();
    },
    
    async createVoyage(voyage) {
        const response = await fetch(`${API_BASE}/voyages`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(voyage)
        });
        return response.json();
    },
    
    async updateVoyage(id, voyage) {
        const response = await fetch(`${API_BASE}/voyages/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(voyage)
        });
        return response.json();
    },
    
    async deleteVoyage(id) {
        const response = await fetch(`${API_BASE}/voyages/${id}`, {
            method: 'DELETE'
        });
        return response.json();
    },

    // Bookings
    async getBookings() {
        const response = await fetch(`${API_BASE}/bookings`);
        return response.json();
    },
    
    async cancelBooking(id) {
        const response = await fetch(`${API_BASE}/bookings/${id}/cancel`, {
            method: 'POST'
        });
        return response.json();
    },

    // Bot Settings
    async getBotStatus() {
        const response = await fetch(`${API_BASE}/bot/status`);
        return response.json();
    },
    
    async setBotStatus(enabled) {
        const response = await fetch(`${API_BASE}/bot/status`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ enabled })
        });
        return response.json();
    },

    // Analytics
    async getAnalytics() {
        const response = await fetch(`${API_BASE}/analytics`);
        return response.json();
    },

    // Admin Chat
    async sendAdminMessage(message) {
        const response = await fetch(`${API_BASE}/admin/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        return response.json();
    }
};
