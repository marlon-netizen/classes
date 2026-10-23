// Renders every favicon.svg (written by tools/build_site.py) to a 64x64 favicon.png fallback for browsers without SVG icons.
// Run after changing the icons:  node tools/make_icons.js   (needs Playwright + Chromium)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const root = path.resolve(__dirname, '..');
const dirs = ['faith-formation', 'ciencias-sociales', 'math', 'physics', 'teacher'];
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium' });
  const pg = await b.newPage({ viewport: { width: 64, height: 64 }, deviceScaleFactor: 1 });
  for (const d of dirs) {
    const svg = fs.readFileSync(path.join(root, d, 'favicon.svg'), 'utf8');
    await pg.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg ', '<svg width="64" height="64" ')}</body></html>`);
    await pg.screenshot({ path: path.join(root, d, 'favicon.png'), omitBackground: true, clip: { x: 0, y: 0, width: 64, height: 64 } });
    console.log('wrote', d + '/favicon.png');
  }
  await b.close();
})();
