// ===================== ANIMATED COUNTERS =====================
function animateCounter(el) {
    const target = parseInt(el.dataset.target, 10);
    const duration = 1200;
    const startTime = performance.now();
    const startVal = 0;

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 4);
        el.textContent = Math.round(startVal + (target - startVal) * eased);
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

function initCounters() {
    const counters = document.querySelectorAll('[data-target]');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.animated) {
                entry.target.dataset.animated = 'true';
                animateCounter(entry.target);
            }
        });
    }, { threshold: 0.3 });
    counters.forEach(c => observer.observe(c));
}

// ===================== LIVE CLOCK =====================
function updateClock() {
    const el = document.getElementById('live-clock');
    if (!el) return;
    const now = new Date();
    const h = String(now.getHours()).padStart(2, '0');
    const m = String(now.getMinutes()).padStart(2, '0');
    const s = String(now.getSeconds()).padStart(2, '0');
    el.textContent = `${h}:${m}:${s}`;
}

// ===================== MESSAGES AUTO-DISMISS =====================
function initMessages() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 500);
        }, 4500);
    });
}

// ===================== AJAX STATUS UPDATE =====================
function updateLogStatus(logId, status) {
    const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
    const btn = document.querySelector(`[data-log-id="${logId}"][data-status="${status}"]`);
    if (btn) btn.classList.add('loading');

    fetch(`/logs/${logId}/status/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: `status=${status}`
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            const row = document.getElementById(`log-row-${logId}`);
            if (row) {
                const statusCell = row.querySelector('.log-status');
                if (statusCell) {
                    const badgeMap = {
                        taken: 'badge-emerald', missed: 'badge-red',
                        skipped: 'badge-amber', pending: 'badge-blue'
                    };
                    const iconMap = {
                        taken: '✅', missed: '❌', skipped: '⏭️', pending: '⏳'
                    };
                    statusCell.innerHTML = `<span class="badge ${badgeMap[status]}">${iconMap[status]} ${status.charAt(0).toUpperCase() + status.slice(1)}</span>`;
                }
            }
            showToast(`Status updated to "${status}"`, 'success');
        }
    })
    .catch(() => showToast('Failed to update status', 'error'))
    .finally(() => {
        if (btn) btn.classList.remove('loading');
    });
}

// ===================== TOAST NOTIFICATIONS =====================
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
    toast.innerHTML = `<span>${icons[type] || ''}</span><span>${message}</span>`;
    container.appendChild(toast);

    requestAnimationFrame(() => toast.classList.add('show'));
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 400);
    }, 3500);
}

function createToastContainer() {
    const c = document.createElement('div');
    c.id = 'toast-container';
    document.body.appendChild(c);
    return c;
}

// ===================== SIDEBAR ACTIVE STATE =====================
function setActiveSidebarLink() {
    const path = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href && href !== '/' && path.startsWith(href)) {
            link.classList.add('active');
        } else if (href === '/' && path === '/') {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// ===================== TIME CHECKBOXES =====================
function initTimeCheckboxes() {
    // Wrap each checkbox in a styled label
    const container = document.querySelector('.time-checkbox-grid');
    if (!container) return;

    const checkboxes = container.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(cb => {
        if (cb.parentElement.classList.contains('time-checkbox-label')) return;
        const wrapper = document.createElement('label');
        wrapper.className = 'time-checkbox-label';
        wrapper.htmlFor = cb.id;
        cb.parentNode.insertBefore(wrapper, cb);
        wrapper.appendChild(cb);
        wrapper.appendChild(document.createTextNode(' ' + cb.nextSibling?.textContent?.trim() || ''));
    });
}

// ===================== COLOR PREVIEW =====================
function initColorPreviews() {
    const colorSelect = document.getElementById('id_avatar_color') || document.getElementById('id_color_tag');
    if (!colorSelect) return;

    const preview = document.createElement('div');
    preview.style.cssText = 'width:24px;height:24px;border-radius:50%;display:inline-block;margin-left:8px;vertical-align:middle;transition:background 0.3s;';
    colorSelect.parentNode.insertBefore(preview, colorSelect.nextSibling);

    function updatePreview() {
        preview.style.background = colorSelect.value;
    }

    colorSelect.addEventListener('change', updatePreview);
    updatePreview();
}

// ===================== FADE IN ELEMENTS =====================
function initFadeIns() {
    const els = document.querySelectorAll('.fade-in');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    els.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });
}

// ===================== INIT =====================
document.addEventListener('DOMContentLoaded', () => {
    initCounters();
    initMessages();
    initFadeIns();
    initColorPreviews();
    setActiveSidebarLink();

    updateClock();
    setInterval(updateClock, 1000);

    // Global event delegation for status updates
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-log-id][data-status]');
        if (btn) {
            const logId = btn.dataset.logId;
            const status = btn.dataset.status;
            updateLogStatus(logId, status);
        }
    });
});

// ===================== TOAST STYLES (injected) =====================
const toastStyle = document.createElement('style');
toastStyle.textContent = `
    #toast-container {
        position: fixed;
        bottom: 24px;
        right: 24px;
        display: flex;
        flex-direction: column;
        gap: 8px;
        z-index: 9999;
    }
    .toast {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px 18px;
        border-radius: 10px;
        font-size: 14px;
        font-weight: 500;
        background: #1a2340;
        border: 1px solid rgba(255,255,255,0.1);
        color: #f0f4ff;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        transform: translateX(120%);
        opacity: 0;
        transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
        min-width: 220px;
        max-width: 340px;
    }
    .toast.show { transform: translateX(0); opacity: 1; }
    .toast-success { border-color: rgba(16,185,129,0.3); }
    .toast-error { border-color: rgba(239,68,68,0.3); }
    .toast-info { border-color: rgba(59,130,246,0.3); }
    .btn.loading { opacity: 0.6; pointer-events: none; }
`;
document.head.appendChild(toastStyle);
