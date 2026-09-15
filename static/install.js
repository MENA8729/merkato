// 1. Register the service worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker
            .register('/static/sw.js')
            .catch(console.error);
    });
}

// 2. Capture the install prompt
let deferredPrompt = null;
const installBtn = document.getElementById('install-btn');

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;

    if (installBtn) {
        installBtn.style.display = 'inline-block';
    }
});

if (installBtn) {
    installBtn.addEventListener('click', async () => {
        if (!deferredPrompt) return;

        deferredPrompt.prompt();

        const { outcome } = await deferredPrompt.userChoice;

        console.log('Install prompt outcome:', outcome);

        deferredPrompt = null;
        installBtn.style.display = 'none';
    });
}

// 3. Hide button once installed
window.addEventListener('appinstalled', () => {
    if (installBtn) {
        installBtn.style.display = 'none';
    }

    console.log('App installed');
});

// 4. iOS Safari manual instructions
const isIOS =
    /iphone|ipad|ipod/.test(window.navigator.userAgent.toLowerCase());

const isInStandaloneMode =
    window.matchMedia('(display-mode: standalone)').matches ||
    window.navigator.standalone;

if (isIOS && !isInStandaloneMode) {
    const banner = document.createElement('div');

    banner.textContent =
        '📲 Install this app: tap Share, then "Add to app"';

    banner.style.cssText =
        'position:fixed;bottom:0;left:0;right:0;' +
        'background:#6366F1;color:#fff;padding:12px;' +
        'text-align:center;font-size:14px;z-index:9999;';

    document.body.appendChild(banner);
}