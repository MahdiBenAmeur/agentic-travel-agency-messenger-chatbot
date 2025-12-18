// API Configuration
const API_BASE = 'http://localhost:8000';

// API Service
const api = {
    // Trips (Voyages)
    async getVoyages() {
        const response = await fetch(`${API_BASE}/trips`);
        if (!response.ok) throw new Error('Failed to fetch trips');
        return response.json();
    },
    
    async createVoyage(voyage) {
        // Map frontend fields to backend schema
        const trip = {
            title: `${voyage.destination} Trip`,
            origin: 'Default Origin', // You may want to add this field to the form
            destination: voyage.destination,
            departure_time: new Date(voyage.start_date).toISOString(),
            arrival_time: new Date(voyage.end_date).toISOString(),
            price: voyage.price,
            available_seats: voyage.capacity,
            is_active: true
        };
        
        const response = await fetch(`${API_BASE}/trips`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(trip)
        });
        if (!response.ok) throw new Error('Failed to create trip');
        return response.json();
    },
    
    async updateVoyage(id, voyage) {
        const trip = {
            title: `${voyage.destination} Trip`,
            origin: 'Default Origin',
            destination: voyage.destination,
            departure_time: new Date(voyage.start_date).toISOString(),
            arrival_time: new Date(voyage.end_date).toISOString(),
            price: voyage.price,
            available_seats: voyage.capacity
        };
        
        const response = await fetch(`${API_BASE}/trips/${id}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(trip)
        });
        if (!response.ok) throw new Error('Failed to update trip');
        return response.json();
    },
    
    async deleteVoyage(id) {
        const response = await fetch(`${API_BASE}/trips/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete trip');
        return response.json();
    },

    // Bookings
    async getBookings() {
        const response = await fetch(`${API_BASE}/bookings`);
        if (!response.ok) throw new Error('Failed to fetch bookings');
        return response.json();
    },
    
    async createBooking(booking) {
        const response = await fetch(`${API_BASE}/bookings`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(booking)
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create booking');
        }
        return response.json();
    },
    
    async confirmBooking(id) {
        const response = await fetch(`${API_BASE}/bookings/${id}/confirm`, {
            method: 'POST'
        });
        if (!response.ok) throw new Error('Failed to confirm booking');
        return response.json();
    },
    
    async cancelBooking(id) {
        const response = await fetch(`${API_BASE}/bookings/${id}/cancel`, {
            method: 'POST'
        });
        if (!response.ok) throw new Error('Failed to cancel booking');
        return response.json();
    },

    // Clients
    async getClients() {
        const response = await fetch(`${API_BASE}/clients`);
        if (!response.ok) throw new Error('Failed to fetch clients');
        return response.json();
    },

    async createClient(client) {
        const response = await fetch(`${API_BASE}/clients`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(client)
        });
        if (!response.ok) throw new Error('Failed to create client');
        return response.json();
    },

    async updateClient(id, client) {
        const response = await fetch(`${API_BASE}/clients/${id}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(client)
        });
        if (!response.ok) throw new Error('Failed to update client');
        return response.json();
    },

    async deleteClient(id) {
        const response = await fetch(`${API_BASE}/clients/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete client');
        return response.json();
    },

    // Messages
    async getRecentMessages(clientId, limit = 20) {
        const response = await fetch(`${API_BASE}/messages/recent/${clientId}?limit=${limit}`);
        if (!response.ok) throw new Error('Failed to fetch messages');
        return response.json();
    },

    // Analytics (placeholder - you'll need to implement this endpoint)
    async getAnalytics() {
        try {
            // Try to fetch real analytics
            const [trips, bookings, clients] = await Promise.all([
                this.getVoyages(),
                this.getBookings(),
                this.getClients()
            ]);
            
            const activeTrips = trips.filter(t => t.is_active).length;
            
            // Calculate revenue by matching booking trip_id with actual trips
            const totalRevenue = bookings
                .filter(b => b.status === 'confirmed')
                .reduce((sum, b) => {
                    // Find the trip by ID to get the price
                    const trip = trips.find(t => t.id === b.trip_id);
                    const tripPrice = trip?.price || 0;
                    const passengers = b.passengers_count || 1;
                    return sum + (tripPrice * passengers);
                }, 0);
            
            // Count actual conversations by checking which clients have messages
            let conversationCount = 0;
            try {
                // Get messages for each client to count active conversations
                const messageChecks = await Promise.all(
                    clients.map(async (client) => {
                        try {
                            const messages = await this.getRecentMessages(client.id, 1);
                            return messages.length > 0 ? 1 : 0;
                        } catch {
                            return 0;
                        }
                    })
                );
                conversationCount = messageChecks.reduce((sum, count) => sum + count, 0);
            } catch (error) {
                console.log('Could not fetch message data, using client count as fallback');
                conversationCount = clients.length;
            }
            
            return {
                total_bookings: bookings.length,
                active_voyages: activeTrips,
                total_revenue: totalRevenue,
                total_conversations: conversationCount
            };
        } catch (error) {
            console.error('Analytics error:', error);
            return {
                total_bookings: 0,
                active_voyages: 0,
                total_revenue: 0,
                total_conversations: 0
            };
        }
    },

    // Bot Settings (placeholder)
    async getBotStatus() {
        // This endpoint doesn't exist yet - return default
        return { enabled: true };
    },
    
    async setBotStatus(enabled) {
        // Placeholder - would need to be implemented in backend
        console.log('Bot status:', enabled);
        return { enabled };
    },

    // Admin Chat (placeholder)
    async sendAdminMessage(message) {
        // Placeholder - would need AI agent integration
        return { 
            response: 'Admin chat not yet implemented. This would query the AI agent for analytics and data.'
        };
    }
};
