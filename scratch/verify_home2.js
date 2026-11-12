const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const ARTIFACT_DIR = 'C:/Users/Tamiluuu/.gemini/antigravity/brain/06550e15-1d17-40fa-9d03-f88f9e6a91ed';
const CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = 9444;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    http.get(url, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

async function run() {
  const chromeProc = spawn(CHROME_PATH, [
    `--remote-debugging-port=${PORT}`,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--hide-scrollbars',
    '--window-size=1440,900'
  ]);

  let wsUrl = null;
  for (let i = 0; i < 20; i++) {
    await sleep(500);
    try {
      const list = await fetchJson(`http://127.0.0.1:${PORT}/json/list`);
      const page = list.find(t => t.type === 'page');
      if (page && page.webSocketDebuggerUrl) {
        wsUrl = page.webSocketDebuggerUrl;
        break;
      }
    } catch (e) {
      // Chrome starting up
    }
  }

  if (!wsUrl) {
    chromeProc.kill();
    throw new Error('Could not connect to Chrome DevTools port');
  }

  console.log('Connected to Chrome DevTools at', wsUrl);

  const ws = new WebSocket(wsUrl);
  let id = 1;
  const callbacks = new Map();
  const consoleErrors = [];

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && callbacks.has(msg.id)) {
      callbacks.get(msg.id)(msg);
      callbacks.delete(msg.id);
    }
    if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
      consoleErrors.push(msg.params.args.map(a => a.value || a.description).join(' '));
    }
    if (msg.method === 'Runtime.exceptionThrown') {
      consoleErrors.push(msg.params.exceptionDetails.text + ' ' + (msg.params.exceptionDetails.exception?.description || ''));
    }
  };

  const send = (method, params = {}) => new Promise((resolve) => {
    const msgId = id++;
    callbacks.set(msgId, resolve);
    ws.send(JSON.stringify({ id: msgId, method, params }));
  });

  await new Promise(r => ws.onopen = r);

  await send('Page.enable');
  await send('Runtime.enable');
  await send('DOM.enable');

  // Set viewport
  await send('Emulation.setDeviceMetricsOverride', {
    width: 1440,
    height: 900,
    deviceScaleFactor: 1,
    mobile: false
  });

  const fileUrl = 'file:///' + path.resolve('home-2.html').replace(/\\/g, '/');
  console.log('Navigating to', fileUrl);
  await send('Page.navigate', { url: fileUrl });

  // Wait for load
  await sleep(2500);

  // Evaluate page status
  const pageEval = await send('Runtime.evaluate', {
    expression: `(() => {
      const sections = ['#home2Hero', '#home2FirstBoil', '#home2Flavour', '#home2Communal', '#home2Craft', '#home2Invitation'];
      const secResults = sections.map(id => {
        const el = document.querySelector(id);
        return { id, exists: !!el, bounds: el ? { y: el.offsetTop, height: el.offsetHeight } : null };
      });

      const images = Array.from(document.querySelectorAll('.home2-main img')).map(img => ({
        src: img.getAttribute('src'),
        complete: img.complete,
        naturalWidth: img.naturalWidth,
        naturalHeight: img.naturalHeight
      }));

      const docWidth = document.documentElement.scrollWidth;
      const winWidth = window.innerWidth;
      const hasHorizontalOverflow = docWidth > winWidth;

      return {
        secResults,
        images,
        docWidth,
        winWidth,
        hasHorizontalOverflow,
        title: document.title
      };
    })()`,
    returnByValue: true
  });

  const pageCheck = pageEval.result ? pageEval.result.result.value : pageEval.result;
  console.log('Page verification check:', JSON.stringify(pageCheck, null, 2));

  // Trigger reveal elements so animations show in screenshots
  await send('Runtime.evaluate', {
    expression: `document.querySelectorAll('.home2-fade-in').forEach(el => el.classList.add('is-visible'))`
  });

  await sleep(600);

  // Capture Section 1 Screenshot (Hero & Navbar)
  const heroShot = await send('Page.captureScreenshot', {
    format: 'png',
    clip: { x: 0, y: 0, width: 1440, height: 950, scale: 1 }
  });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'home2_sec1_hero.png'), Buffer.from(heroShot.result.data, 'base64'));
  console.log('Saved home2_sec1_hero.png');

  // Capture Section 2 & 3 Screenshot
  const sec2Bounds = pageCheck.secResults[1].bounds;
  if (sec2Bounds) {
    await send('Runtime.evaluate', { expression: `window.scrollTo(0, ${sec2Bounds.y})` });
    await sleep(400);
    const sec2Shot = await send('Page.captureScreenshot', {
      format: 'png'
    });
    fs.writeFileSync(path.join(ARTIFACT_DIR, 'home2_sec2_boil.png'), Buffer.from(sec2Shot.result.data, 'base64'));
    console.log('Saved home2_sec2_boil.png');
  }

  // Capture Section 4 & 5 Screenshot
  const sec4Bounds = pageCheck.secResults[3].bounds;
  if (sec4Bounds) {
    await send('Runtime.evaluate', { expression: `window.scrollTo(0, ${sec4Bounds.y})` });
    await sleep(400);
    const sec4Shot = await send('Page.captureScreenshot', {
      format: 'png'
    });
    fs.writeFileSync(path.join(ARTIFACT_DIR, 'home2_sec4_table.png'), Buffer.from(sec4Shot.result.data, 'base64'));
    console.log('Saved home2_sec4_table.png');
  }

  // Capture Section 6 Screenshot
  const sec6Bounds = pageCheck.secResults[5].bounds;
  if (sec6Bounds) {
    await send('Runtime.evaluate', { expression: `window.scrollTo(0, ${sec6Bounds.y})` });
    await sleep(400);
    const sec6Shot = await send('Page.captureScreenshot', {
      format: 'png'
    });
    fs.writeFileSync(path.join(ARTIFACT_DIR, 'home2_sec6_invitation.png'), Buffer.from(sec6Shot.result.data, 'base64'));
    console.log('Saved home2_sec6_invitation.png');
  }

  // Switch to Light Mode and capture hero
  await send('Runtime.evaluate', {
    expression: `window.scrollTo(0, 0); document.documentElement.setAttribute('data-theme', 'light');`
  });
  await sleep(600);

  const lightShot = await send('Page.captureScreenshot', {
    format: 'png'
  });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'home2_light_mode.png'), Buffer.from(lightShot.result.data, 'base64'));
  console.log('Saved home2_light_mode.png');

  // Test Mobile 375px
  await send('Runtime.evaluate', {
    expression: `window.scrollTo(0, 0); document.documentElement.setAttribute('data-theme', 'dark');`
  });
  await send('Emulation.setDeviceMetricsOverride', {
    width: 375,
    height: 812,
    deviceScaleFactor: 2,
    mobile: true
  });
  await sleep(600);

  const mobileCheck = await send('Runtime.evaluate', {
    expression: `(() => {
      return {
        docWidth: document.documentElement.scrollWidth,
        winWidth: window.innerWidth,
        hasHorizontalOverflow: document.documentElement.scrollWidth > window.innerWidth
      };
    })()`,
    returnByValue: true
  });
  const mobileVal = mobileCheck.result ? (mobileCheck.result.result ? mobileCheck.result.result.value : mobileCheck.result.value) : null;
  console.log('Mobile 375px check:', mobileVal);

  const mobileShot = await send('Page.captureScreenshot', {
    format: 'png'
  });
  fs.writeFileSync(path.join(ARTIFACT_DIR, 'home2_mobile_375.png'), Buffer.from(mobileShot.result.data, 'base64'));
  console.log('Saved home2_mobile_375.png');

  console.log('\n--- Console Errors: ' + consoleErrors.length + ' ---');
  consoleErrors.forEach(err => console.error('Console error:', err));

  ws.close();
  chromeProc.kill();
}

run().catch(err => {
  console.error('Error during verification:', err);
  process.exit(1);
});
