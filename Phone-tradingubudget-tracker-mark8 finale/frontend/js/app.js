// Main Application Logic
import * as api from './api.js';
import { 
    createPhoneCard, 
    showToast, 
    updateBudgetDisplay, 
    updateStatsDisplay 
} from './components.js';

// Application State
let phones = [];
let budget = { total_money: 0 };
let stats = {};
let loading = false;
let hiddenPhoneIds = new Set(); // NEW: Track hidden phone IDs

// DOM Elements
const elements = {
    budgetForm: document.getElementById('budget-form'),
    budgetInput: document.getElementById('budget-input'),
    updateBudgetBtn: document.getElementById('update-budget-btn'),
    cancelBudgetBtn: document.getElementById('cancel-budget-btn'),
    settingsBtn: document.getElementById('settings-btn'),
    
    addPhoneBtn: document.getElementById('add-phone-btn'),
    addPhoneForm: document.getElementById('add-phone-form'),
    submitPhoneBtn: document.getElementById('submit-phone-btn'),
    cancelPhoneBtn: document.getElementById('cancel-phone-btn'),
    getStartedBtn: document.getElementById('get-started-btn'),
    
    phoneBrand: document.getElementById('phone-brand'),
    phoneModel: document.getElementById('phone-model'),
    phonePrice: document.getElementById('phone-price'),
    phoneNotes: document.getElementById('phone-notes'),
    
    phonesGrid: document.getElementById('phones-grid'),
    emptyState: document.getElementById('empty-state')
};

// Initialize Application
async function init() {
    attachEventListeners();
    await fetchAllData();
}

// Fetch all data from backend
async function fetchAllData() {
    try {
        const [phonesData, budgetData, statsData] = await Promise.all([
            api.getPhones(),
            api.getBudget(),
            api.getStats()
        ]);
        
        phones = phonesData;
        budget = budgetData;
        stats = statsData;
        
        renderPhones();
        updateBudgetDisplay(budget);
        updateStatsDisplay(stats);
    } catch (error) {
        console.error('Error fetching data:', error);
        showToast('Failed to load data', 'error');
    }
}

// Render phones grid
function renderPhones() {
    elements.phonesGrid.innerHTML = '';
    
    // Filter out hidden phones for display only
    const visiblePhones = phones.filter(phone => !hiddenPhoneIds.has(phone.id));
    
    if (visiblePhones.length === 0) {
        elements.emptyState.classList.remove('hidden');
        elements.phonesGrid.classList.add('hidden');
    } else {
        elements.emptyState.classList.add('hidden');
        elements.phonesGrid.classList.remove('hidden');
        
        visiblePhones.forEach(phone => {
            const phoneCard = createPhoneCard(phone, handleStateChange, handleHidePhone);
            elements.phonesGrid.appendChild(phoneCard);
        });
    }
}

// Handle hiding a phone (frontend only)
function handleHidePhone(phone) {
    hiddenPhoneIds.add(phone.id);
    renderPhones();
    showToast(`${phone.brand} ${phone.model} hidden from view`, 'info');
}

// Event Listeners
function attachEventListeners() {
    // Budget form
    elements.settingsBtn.addEventListener('click', toggleBudgetForm);
    elements.updateBudgetBtn.addEventListener('click', handleUpdateBudget);
    elements.cancelBudgetBtn.addEventListener('click', () => {
        elements.budgetForm.classList.add('hidden');
        elements.budgetInput.value = '';
    });
    
    // Phone form
    elements.addPhoneBtn.addEventListener('click', togglePhoneForm);
    elements.getStartedBtn.addEventListener('click', togglePhoneForm);
    elements.submitPhoneBtn.addEventListener('click', handleAddPhone);
    elements.cancelPhoneBtn.addEventListener('click', () => {
        elements.addPhoneForm.classList.add('hidden');
        clearPhoneForm();
    });
    
    // Enter key submission
    elements.budgetInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleUpdateBudget();
    });
}

function toggleBudgetForm() {
    elements.budgetForm.classList.toggle('hidden');
    if (!elements.budgetForm.classList.contains('hidden')) {
        elements.budgetInput.focus();
    }
}

function togglePhoneForm() {
    elements.addPhoneForm.classList.toggle('hidden');
    if (!elements.addPhoneForm.classList.contains('hidden')) {
        elements.phoneBrand.focus();
    }
}

// Handle budget update
async function handleUpdateBudget() {
    const amount = parseFloat(elements.budgetInput.value);
    
    if (isNaN(amount)) {
        showToast('Please enter a valid amount', 'warning');
        return;
    }
    
    if (loading) return;
    loading = true;
    elements.updateBudgetBtn.disabled = true;
    
    try {
        await api.updateBudget(amount);
        showToast('Budget updated successfully!', 'success');
        elements.budgetForm.classList.add('hidden');
        elements.budgetInput.value = '';
        await fetchAllData();
    } catch (error) {
        console.error('Error updating budget:', error);
        showToast('Failed to update budget', 'error');
    } finally {
        loading = false;
        elements.updateBudgetBtn.disabled = false;
    }
}

// Handle add phone
async function handleAddPhone() {
    const brand = elements.phoneBrand.value.trim();
    const model = elements.phoneModel.value.trim();
    const price = parseFloat(elements.phonePrice.value);
    const notes = elements.phoneNotes.value.trim();
    
    if (!brand || !model || isNaN(price)) {
        showToast('Please fill in all required fields', 'warning');
        return;
    }
    
    if (loading) return;
    loading = true;
    elements.submitPhoneBtn.disabled = true;
    
    try {
        const data = await api.addPhone({
            brand,
            model,
            buy_price: price,
            notes
        });
        
        if (data.messages && data.messages.length > 0) {
            data.messages.forEach(msg => showToast(msg.message, msg.type));
        } else {
            showToast('Phone added successfully!', 'success');
        }
        
        elements.addPhoneForm.classList.add('hidden');
        clearPhoneForm();
        await fetchAllData();
    } catch (error) {
        console.error('Error adding phone:', error);
        showToast('Failed to add phone', 'error');
    } finally {
        loading = false;
        elements.submitPhoneBtn.disabled = false;
    }
}

function clearPhoneForm() {
    elements.phoneBrand.value = '';
    elements.phoneModel.value = '';
    elements.phonePrice.value = '';
    elements.phoneNotes.value = '';
}

// Handle phone state change
async function handleStateChange(phone, newState) {
    let sellPrice = null;
    
    if (newState === 'sold' || (phone.state === 'scammed' && newState === 'sold')) {
        const input = prompt('Enter the selling price:');
        if (!input || isNaN(input) || parseFloat(input) <= 0) {
            showToast('Please enter a valid selling price', 'warning');
            return;
        }
        sellPrice = parseFloat(input);
    }
    
    if (loading) return;
    loading = true;
    
    try {
        const body = { state: newState };
        if (sellPrice !== null) body.sell_price = sellPrice;
        
        const data = await api.updatePhoneState(phone.id, body);
        
        if (data.messages && data.messages.length > 0) {
            data.messages.forEach(msg => showToast(msg.message, msg.type));
        } else {
            showToast('Phone state updated!', 'success');
        }
        
        await fetchAllData();
    } catch (error) {
        console.error('Error updating phone state:', error);
        showToast('Failed to update phone state', 'error');
    } finally {
        loading = false;
    }
}

// Start the application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

