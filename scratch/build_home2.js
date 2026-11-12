const fs = require('fs');
const path = require('path');

const navbarHtml = fs.readFileSync('navbar.html', 'utf8');
const lines = navbarHtml.split('\n');

const home2Css = fs.readFileSync('scratch/home2_css.css', 'utf8');
const home2Html = fs.readFileSync('scratch/home2_html.html', 'utf8');
const home2Js = fs.readFileSync('scratch/home2_js.js', 'utf8');

// Find boundaries
let styleStart = -1;
let styleEnd = -1;
let mainStart = -1;
let mainEnd = -1;
let scriptStart = -1;
let scriptEnd = -1;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (line.includes('HOMEPAGE SPECIFIC LUXURY STYLES')) styleStart = i - 1; // including the comment start
  if (line.includes('LUXURY HOT POT RESTAURANT FOOTER STYLES')) styleEnd = i - 1;
  if (line.includes('<main class="hp-main"')) mainStart = i;
  if (line.includes('</main>')) mainEnd = i;
  if (line.includes('HOMEPAGE INTERACTIVE LOGIC')) scriptStart = i - 1;
  if (line.trim() === '})();' && i > 4950) scriptEnd = i;
}

console.log({ styleStart, styleEnd, mainStart, mainEnd, scriptStart, scriptEnd });

// Part 1: Head & global styles up to styleStart
const part1 = lines.slice(0, styleStart).join('\n');

// Part 2: Footer styles & navbar markup from styleEnd to mainStart
const part2 = lines.slice(styleEnd, mainStart).join('\n');

// Part 3: Footer HTML & core scripts from (mainEnd + 1) to scriptStart
const part3 = lines.slice(mainEnd + 1, scriptStart).join('\n');

// Part 4: Script close & body/html end from scriptEnd
const part4 = lines.slice(scriptEnd).join('\n');

// Assemble complete document
const outputHtml = [
  part1,
  '\n    /* ==========================================================================\n       HOMEPAGE 2 SPECIFIC LUXURY STYLES\n       ========================================================================== */\n',
  home2Css,
  '\n',
  part2,
  '\n',
  home2Html,
  '\n',
  part3,
  '\n',
  home2Js,
  '\n',
  part4
].join('');

fs.writeFileSync('home-2.html', outputHtml, 'utf8');
console.log('Successfully generated home-2.html, size:', outputHtml.length, 'bytes');
