const puppeteer = require('puppeteer-core');
const { AxePuppeteer } = require('@axe-core/puppeteer');

const targetUrl = process.argv[2] || 'https://example.com';

(async () => {
    console.log(`[+] Launching WCAG 2.1 AA Accessibility Audit against: ${targetUrl}`);

    const browser = await puppeteer.launch({
        executablePath: '/usr/bin/chromium',
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    try {
        await page.goto(targetUrl, { waitUntil: 'networkidle2', timeout: 30000 });
        const results = await new AxePuppeteer(page)
            .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
            .analyze();

        await browser.close();

        console.log(`\n=== ♿ WCAG ACCESSIBILITY AUDIT REPORT ===`);
        console.log(`Target:         ${targetUrl}`);
        console.log(`Passed Rules:   ${results.passes.length}`);
        console.log(`Violations:     ${results.violations.length}`);

        if (results.violations.length === 0) {
            console.log(`\n[✓] Zero WCAG 2.1 AA violations detected!`);
            return;
        }

        const counts = { critical: 0, serious: 0, moderate: 0, minor: 0 };
        results.violations.forEach(v => {
            if (counts[v.impact] !== undefined) counts[v.impact]++;
        });

        console.log(`\nSeverity Breakdown:`);
        console.log(`  - Critical: ${counts.critical}`);
        console.log(`  - Serious:  ${counts.serious}`);
        console.log(`  - Moderate: ${counts.moderate}`);
        console.log(`  - Minor:    ${counts.minor}`);

        console.log(`\n--- Detailed Violations (Ready for Non-Functional Report) ---`);
        results.violations.forEach((v, idx) => {
            console.log(`\n[#${idx + 1}] [${(v.impact || 'UNKNOWN').toUpperCase()}] ${v.id}: ${v.help}`);
            console.log(`  Description: ${v.description}`);
            console.log(`  Help URL:    ${v.helpUrl}`);
            console.log(`  Affected Elements (${v.nodes.length}):`);
            v.nodes.slice(0, 3).forEach(node => {
                console.log(`    * Target: ${node.target.join(' ')}`);
                console.log(`      HTML:   ${node.html.substring(0, 100)}...`);
                console.log(`      Fix:    ${node.failureSummary ? node.failureSummary.split('\n')[0] : 'N/A'}`);
            });
            if (v.nodes.length > 3) {
                console.log(`    * ... and ${v.nodes.length - 3} more elements`);
            }
        });

        console.log(`\n[✓] Audit complete.`);
    } catch (e) {
        console.error(`[!] Audit error: ${e.message}`);
        await browser.close();
    }
})();
