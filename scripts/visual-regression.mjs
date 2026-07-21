import { chromium, devices } from 'playwright';
import fs from 'node:fs/promises';

const baseURL = process.env.BASE_URL || 'http://127.0.0.1:4173';
await fs.mkdir('screenshots', { recursive: true });

const browser = await chromium.launch({ headless: true });

async function capture(name, contextOptions, path, setup) {
  const context = await browser.newContext(contextOptions);
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(`pageerror: ${error.message}`));
  page.on('console', message => {
    if (message.type() === 'error') errors.push(`console: ${message.text()}`);
  });

  await page.goto(`${baseURL}/${path}`, { waitUntil: 'networkidle' });
  await page.emulateMedia({ reducedMotion: 'reduce' });
  if (setup) await setup(page);
  await page.screenshot({ path: `screenshots/${name}.png`, fullPage: true });

  if (errors.length) {
    await fs.writeFile(`screenshots/${name}-errors.txt`, errors.join('\n'));
    throw new Error(`${name} produced browser errors:\n${errors.join('\n')}`);
  }
  await context.close();
}

await capture(
  'home-desktop',
  { viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 },
  'index.html',
  async page => {
    await page.locator('#mood-input').fill('今天也想慢一点');
    await page.locator('#mood-input').press('Enter');
    await page.waitForTimeout(900);
  },
);

await capture(
  'home-mobile',
  { ...devices['iPhone 13'] },
  'index.html',
  async page => {
    await page.locator('#mood-input').fill('有一点累');
    await page.locator('#mood-input').press('Enter');
    await page.waitForTimeout(900);
  },
);

await capture(
  'settings-desktop',
  { viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 },
  'settings.html',
);

await capture(
  'settings-mobile',
  { ...devices['iPhone 13'] },
  'settings.html',
);

await browser.close();
console.log('Visual regression screenshots created successfully.');
