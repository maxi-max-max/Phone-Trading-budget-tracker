// API Module - All Flask backend calls

const API_BASE = '/api';

async function handleResponse(response) {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

export async function getPhones() {
    const response = await fetch(`${API_BASE}/phones`);
    return handleResponse(response);
}

export async function getBudget() {
    const response = await fetch(`${API_BASE}/budget`);
    return handleResponse(response);
}

export async function getStats() {
    const response = await fetch(`${API_BASE}/stats`);
    return handleResponse(response);
}

export async function addPhone(phoneData) {
    const response = await fetch(`${API_BASE}/phones`, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(phoneData)
    });
    return handleResponse(response);
}

export async function updatePhoneState(phoneId, data) {
    const response = await fetch(`${API_BASE}/phones/${phoneId}/state`, {
        method: 'PUT',
        headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return handleResponse(response);
}

export async function updateBudget(totalMoney) {
    const response = await fetch(`${API_BASE}/budget`, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({ total_money: totalMoney })
    });
    return handleResponse(response);
}

export async function deletePhone(phoneId) {
    const response = await fetch(`${API_BASE}/phones/${phoneId}`, {
        method: 'DELETE',
        headers: { 
            'Accept': 'application/json'
        }
    });
    return handleResponse(response);
}

