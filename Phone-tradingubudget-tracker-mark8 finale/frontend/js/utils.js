// Helper Functions

export function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount || 0);
}

export function getStateBadgeClass(state) {
    const classes = {
        bought: 'badge-bought',
        sold: 'badge-sold',
        scammed: 'badge-scammed'
    };
    return classes[state] || 'badge-bought';
}

export function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}