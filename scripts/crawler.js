const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const targetUrl = process.argv[2] || 'https://example.com';
const evidenceDir = path.resolve(__dirname, '../evidence');

if (!fs.existsSync(evidenceDir)) {
    fs.mkdirSync(evidenceDir, { recursive: true });
}

(async () => {
    console.log(`[+] Initializing SUT crawler against: ${targetUrl}`);
    const browser = await puppeteer.launch({
        executablePath: '/usr/bin/chromium',
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    const consoleLogs = [];
    const networkErrors = [];
    const apiRequests = [];

    page.on('console', msg => {
        consoleLogs.push({ type: msg.type(), text: msg.text() });
    });

    page.on('requestfailed', request => {
        networkErrors.push({
            url: request.url(),
            failure: request.failure() ? request.failure().errorText : 'Unknown failure'
        });
    });

    page.on('response', response => {
        const status = response.status();
        const url = response.url();
        if (status >= 400) {
            networkErrors.push({ url, status, statusText: response.statusText() });
        }
        if (url.includes('/api/') || url.includes('/v1/') || url.includes('.json')) {
            apiRequests.push({ url, status });
        }
    });

    const startTime = Date.now();
    try {
        await page.goto(targetUrl, { waitUntil: 'networkidle2', timeout: 30000 });
    } catch (e) {
        console.error(`[!] Navigation notice: ${e.message}`);
    }
    const loadTimeMs = Date.now() - startTime;

    // Screenshot
    const domain = new URL(targetUrl).hostname.replace(/[^a-zA-Z0-9]/g, '_');
    const screenshotPath = path.join(evidenceDir, `sut_${domain}_${Date.now()}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: true });

    // Page Metadata & Forms Scraped
    const analysis = await page.evaluate(() => {
        const inputs = Array.from(document.querySelectorAll('input, select, textarea')).map(el => ({
            tag: el.tagName.toLowerCase(),
            type: el.type || '',
            name: el.name || '',
            id: el.id || '',
            placeholder: el.placeholder || '',
            required: el.required
        }));

        const forms = Array.from(document.querySelectorAll('form')).map(f => ({
            action: f.action,
            method: f.method,
            inputCount: f.querySelectorAll('input, select, textarea').length
        }));

        const links = Array.from(document.querySelectorAll('a[href]')).map(a => a.href);
        const buttons = Array.from(document.querySelectorAll('button, input[type="submit"]')).map(b => (b.innerText || b.value || '').trim());

        return {
            title: document.title,
            formsCount: forms.length,
            forms,
            inputsCount: inputs.length,
            inputs,
            linksCount: links.length,
            buttonsCount: buttons.length,
            buttons: buttons.slice(0, 15)
        };
    });

    await browser.close();

    console.log(`\n=== 🎯 SUT DIAGNOSTIC REPORT ===`);
    console.log(`Page Title:      ${analysis.title}`);
    console.log(`Load Duration:   ${loadTimeMs} ms`);
    console.log(`Forms Detected:  ${analysis.formsCount}`);
    console.log(`Input Fields:    ${analysis.inputsCount}`);
    console.log(`Buttons Found:   ${analysis.buttonsCount}`);
    console.log(`Console Errors:  ${consoleLogs.filter(l => l.type === 'error').length}`);
    console.log(`Network Errors:  ${networkErrors.length}`);
    console.log(`Screenshot:      ${screenshotPath}`);

    if (consoleLogs.filter(l => l.type === 'error').length > 0) {
        console.log(`\n[!] Console Errors Detected:`);
        consoleLogs.filter(l => l.type === 'error').forEach(l => console.log(`  - ${l.text}`));
    }

    if (networkErrors.length > 0) {
        console.log(`\n[!] Network / HTTP Errors:`);
        networkErrors.forEach(n => console.log(`  - [${n.status || 'FAIL'}] ${n.url} (${n.failure || n.statusText})`));
    }

    if (analysis.inputs.length > 0) {
        console.log(`\n[+] Discovered Input Fields:`);
        analysis.inputs.forEach(i => console.log(`  - [${i.type || i.tag}] name="${i.name}" id="${i.id}" (required: ${i.required})`));
    }

    console.log(`\n[✓] Diagnostic sweep complete.`);
})();
