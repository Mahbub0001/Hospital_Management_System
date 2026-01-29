// Main JavaScript file for Hospital Management System

function initializeApp() {
    initializeThemeToggle();

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Dynamic form field updates
    initializeDynamicForms();
    
    // Search functionality
    initializeSearch();
    
    // Date picker initialization
    initializeDatePickers();
    
    // Chart initialization
    initializeCharts();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}

function initializeThemeToggle() {
    const toggleBtn = document.getElementById('themeToggle');
    const icon = document.getElementById('themeIcon');

    const applyTheme = (theme, animate = false) => {
        if (animate) {
            document.body.classList.add('theme-switching');
            window.setTimeout(() => document.body.classList.remove('theme-switching'), 450);
        }

        document.documentElement.dataset.theme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        if (document.body) {
            document.body.classList.toggle('theme-dark', theme === 'dark');
            document.body.dataset.theme = theme;
        }
        try {
            localStorage.setItem('theme', theme);
        } catch (e) {
        }

        if (icon) {
            icon.classList.remove('fa-moon', 'fa-sun');
            icon.classList.add(theme === 'dark' ? 'fa-sun' : 'fa-moon');
        }

        if (toggleBtn) {
            toggleBtn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
        }
    };

    const getPreferredTheme = () => {
        try {
            const saved = localStorage.getItem('theme');
            if (saved === 'dark' || saved === 'light') return saved;
        } catch (e) {
        }

        return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    };

    applyTheme(getPreferredTheme(), false);

    const toggle = () => {
        const current = document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light';
        const next = current === 'dark' ? 'light' : 'dark';
        applyTheme(next, true);
    };

    if (toggleBtn) {
        toggleBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            toggle();
        });
    } else {
        // Fallback for pages where the button is injected later
        document.addEventListener('click', (e) => {
            const btn = e.target && (e.target.id === 'themeToggle' ? e.target : e.target.closest ? e.target.closest('#themeToggle') : null);
            if (btn) {
                e.preventDefault();
                toggle();
            }
        });
    }
}

// Dynamic form field updates
function initializeDynamicForms() {
    // Department selection updates doctor options
    const departmentSelect = document.getElementById('id_department');
    const doctorSelect = document.getElementById('id_doctor');
    
    if (departmentSelect && doctorSelect) {
        departmentSelect.addEventListener('change', function() {
            const departmentId = this.value;
            if (departmentId) {
                fetch(`/api/doctors/?department_id=${departmentId}`)
                    .then(response => response.json())
                    .then(data => {
                        doctorSelect.innerHTML = '<option value="">Select Doctor</option>';
                        data.doctors.forEach(doctor => {
                            const option = document.createElement('option');
                            option.value = doctor.id;
                            option.textContent = doctor.name;
                            doctorSelect.appendChild(option);
                        });
                    })
                    .catch(error => console.error('Error fetching doctors:', error));
            } else {
                doctorSelect.innerHTML = '<option value="">Select Department First</option>';
            }
        });
    }
}

// Search functionality
function initializeSearch() {
    const searchInputs = document.querySelectorAll('input[name="search"]');
    searchInputs.forEach(function(input) {
        let searchTimeout;
        
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const searchTerm = this.value;
            
            searchTimeout = setTimeout(function() {
                if (searchTerm.length >= 2 || searchTerm.length === 0) {
                    // Trigger search
                    const form = input.closest('form');
                    if (form) {
                        form.submit();
                    }
                }
            }, 500);
        });
    });
}

// Date picker initialization
function initializeDatePickers() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    
    dateInputs.forEach(function(input) {
        // Set minimum date to today for appointment dates
        if (input.id === 'id_date' && input.closest('form')?.action?.includes('appointment')) {
            input.min = today;
        }
        
        // Add date formatting
        input.addEventListener('change', function() {
            const date = new Date(this.value);
            const formattedDate = date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
            
            // Store formatted date for display
            this.dataset.formatted = formattedDate;
        });
    });
}

// Chart initialization
function initializeCharts() {
    // Only initialize charts on dashboard
    if (document.getElementById('appointmentChart')) {
        // Appointment chart is already initialized in the template
        console.log('Charts initialized');
    }
}

// Utility functions
function showLoadingSpinner(element) {
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    spinner.id = 'loading-spinner';
    element.appendChild(spinner);
}

function hideLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// AJAX form submission
function submitFormAjax(form, successCallback, errorCallback) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.innerHTML;
    
    // Show loading state
    submitButton.disabled = true;
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    
    fetch(form.action, {
        method: form.method,
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (successCallback) successCallback(data);
        } else {
            if (errorCallback) errorCallback(data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (errorCallback) errorCallback({error: 'An unexpected error occurred'});
    })
    .finally(() => {
        // Reset button state
        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonText;
    });
}

// Print functionality
function printElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <html>
                <head>
                    <title>Print</title>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                    <style>
                        body { padding: 20px; }
                        .no-print { display: none !important; }
                        @media print {
                            .no-print { display: none !important; }
                        }
                    </style>
                </head>
                <body>
                    ${element.innerHTML}
                </body>
            </html>
        `);
        printWindow.document.close();
        printWindow.print();
    }
}

// Export to CSV functionality
function exportToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    for (let i = 0; i < rows.length; i++) {
        const row = [];
        const cols = rows[i].querySelectorAll('td, th');
        
        for (let j = 0; j < cols.length; j++) {
            // Remove HTML tags and get text content
            let text = cols[j].textContent.trim();
            // Escape quotes and commas
            text = text.replace(/"/g, '""');
            if (text.includes(',')) {
                text = `"${text}"`;
            }
            row.push(text);
        }
        csv.push(row.join(','));
    }
    
    // Create CSV file
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'export.csv';
    a.click();
    
    window.URL.revokeObjectURL(url);
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl+S to save forms
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        const activeForm = document.querySelector('form:focus-within');
        if (activeForm) {
            activeForm.submit();
        }
    }
    
    // Ctrl+N for new records (when applicable)
    if (e.ctrlKey && e.key === 'n') {
        e.preventDefault();
        const createButton = document.querySelector('a[href*="create"]');
        if (createButton) {
            window.location.href = createButton.href;
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const openModal = document.querySelector('.modal.show');
        if (openModal) {
            const modal = bootstrap.Modal.getInstance(openModal);
            if (modal) {
                modal.hide();
            }
        }
    }
});

// Real-time clock for dashboard
function updateClock() {
    const clockElement = document.getElementById('current-time');
    if (clockElement) {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        const dateString = now.toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        clockElement.innerHTML = `${dateString} ${timeString}`;
    }
}

// Update clock every second
setInterval(updateClock, 1000);
updateClock(); // Initial call

// Form field validation patterns
const validationPatterns = {
    phone: /^[\d\s\-\+\(\)]+$/,
    email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    name: /^[a-zA-Z\s\-']+$/,
    alphanumeric: /^[a-zA-Z0-9\s\-_]+$/
};

// Validate field with pattern
function validateField(field, pattern) {
    const value = field.value.trim();
    const regex = validationPatterns[pattern];
    
    if (regex && !regex.test(value)) {
        field.classList.add('is-invalid');
        return false;
    } else {
        field.classList.remove('is-invalid');
        return true;
    }
}

// Add validation to relevant fields
document.addEventListener('DOMContentLoaded', function() {
    const phoneFields = document.querySelectorAll('input[name*="phone"]');
    phoneFields.forEach(field => {
        field.addEventListener('blur', () => validateField(field, 'phone'));
    });
    
    const emailFields = document.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        field.addEventListener('blur', () => validateField(field, 'email'));
    });
    
    const nameFields = document.querySelectorAll('input[name*="name"]');
    nameFields.forEach(field => {
        field.addEventListener('blur', () => validateField(field, 'name'));
    });
});
