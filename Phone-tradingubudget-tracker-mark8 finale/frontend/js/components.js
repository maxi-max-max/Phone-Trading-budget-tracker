// UI Component Functions
import { formatCurrency, getStateBadgeClass, capitalize } from './utils.js';

export function createPhoneCard(phone, onStateChange, onHidePhone) {
    const card = document.createElement('div');
    card.className = 'phone-card';
    card.dataset.phoneId = phone.id;

    const badgeClass = getStateBadgeClass(phone.state);
    
    card.innerHTML = `
        <div class="phone-header">
            <div class="phone-info">
                <h3>${phone.brand} ${phone.model}</h3>
                <span class="badge ${badgeClass}">${capitalize(phone.state)}</span>
            </div>
            <div class="phone-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect>
                    <line x1="12" y1="18" x2="12" y2="18"></line>
                </svg>
            </div>
        </div>

        <div class="phone-details">
            <div class="detail-row">
                <span class="detail-label">Buy Price:</span>
                <span class="detail-value">${formatCurrency(phone.buy_price)}</span>
            </div>
            ${phone.sell_price ? `
                <div class="detail-row">
                    <span class="detail-label">Sell Price:</span>
                    <span class="detail-value">${formatCurrency(phone.sell_price)}</span>
                </div>
            ` : ''}
            ${phone.profit !== null ? `
                <div class="detail-row">
                    <span class="detail-label">Profit:</span>
                    <span class="detail-value ${phone.profit >= 0 ? 'profit' : 'loss'}">
                        ${formatCurrency(phone.profit)}
                    </span>
                </div>
            ` : ''}
        </div>

        ${phone.notes ? `
            <div class="phone-notes">
                <p>${phone.notes}</p>
            </div>
        ` : ''}

        <div class="phone-actions">
            ${renderActionButtons(phone)}
        </div>
    `;

    // Attach event listeners
    attachCardEventListeners(card, phone, onStateChange, onHidePhone);
    
    return card;
}

function renderActionButtons(phone) {
    let stateButtons = '';
    
    if (phone.state === 'bought') {
        stateButtons = `
            <button class="btn btn-success" data-action="sold">Mark Sold</button>
            <button class="btn btn-danger" data-action="scammed">Mark Scammed</button>
        `;
    } else if (phone.state === 'sold') {
        stateButtons = `
            <button class="btn btn-danger" data-action="scammed">Mark as Scam</button>
        `;
    } else if (phone.state === 'scammed') {
        stateButtons = `
            <button class="btn btn-success" data-action="sold">Actually Sold</button>
        `;
    }
    
    // Add hide button for all states
    return `
        ${stateButtons}
        <button class="btn btn-secondary" data-action="hide" title="Hide from view (doesn't delete)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                <line x1="1" y1="1" x2="23" y2="23"></line>
            </svg>
            Hide
        </button>
    `;
}

function attachCardEventListeners(card, phone, onStateChange, onHidePhone) {
    const buttons = card.querySelectorAll('[data-action]');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const action = button.dataset.action;
            
            if (action === 'hide') {
                onHidePhone(phone);
            } else {
                onStateChange(phone, action);
            }
        });
    });
}

export function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icons = {
        success: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                  </svg>`,
        error: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>`,
        warning: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                    <line x1="12" y1="9" x2="12" y2="13"></line>
                    <line x1="12" y1="17" x2="12.01" y2="17"></line>
                  </svg>`,
        info: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                 <circle cx="12" cy="12" r="10"></circle>
                 <line x1="12" y1="16" x2="12" y2="12"></line>
                 <line x1="12" y1="8" x2="12.01" y2="8"></line>
               </svg>`
    };

    toast.innerHTML = `
        <div class="toast-icon">${icons[type]}</div>
        <div class="toast-message">${message}</div>
        <button class="toast-close">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        </button>
    `;

    container.appendChild(toast);

    // Close button
    toast.querySelector('.toast-close').addEventListener('click', () => {
        toast.remove();
    });

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, 5000);
}

export function updateBudgetDisplay(budget) {
    const budgetElement = document.getElementById('budget-amount');
    budgetElement.textContent = formatCurrency(budget.total_money);
    
    // Update color class
    budgetElement.classList.remove('positive', 'negative');
    if (budget.total_money >= 0) {
        budgetElement.classList.add('positive');
    } else {
        budgetElement.classList.add('negative');
    }
}

export function updateStatsDisplay(stats) {
    document.getElementById('stat-total').textContent = stats.total_bought || 0;
    document.getElementById('stat-sold').textContent = stats.total_sold || 0;
    document.getElementById('stat-profit').textContent = formatCurrency(stats.total_profit);
    document.getElementById('stat-lost').textContent = formatCurrency(stats.total_lost);
    
    // Update profit color
    const profitElement = document.getElementById('stat-profit');
    profitElement.classList.remove('green', 'red');
    if ((stats.total_profit || 0) >= 0) {
        profitElement.classList.add('green');
    } else {
        profitElement.classList.add('red');
    }
}


