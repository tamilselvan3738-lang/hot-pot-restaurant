const fs = require('fs');
const path = require('path');

// 1. Get all images in images/
const imagesDir = path.join(__dirname, '..', 'images');
const allImages = fs.readdirSync(imagesDir);

console.log('Total files in images/:', allImages.length);

// 2. Scan all HTML files for image usage
const htmlFiles = fs.readdirSync(path.join(__dirname, '..')).filter(f => f.endsWith('.html') && f !== 'home-2.html');
const usedImagesMap = {};

htmlFiles.forEach(file => {
  const content = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
  allImages.forEach(img => {
    if (content.includes(img)) {
      if (!usedImagesMap[img]) usedImagesMap[img] = [];
      usedImagesMap[img].push(file);
    }
  });
});

console.log('Images used across other HTML pages:', Object.keys(usedImagesMap).length);
console.log('Unused images in images/:');
const unused = allImages.filter(img => !usedImagesMap[img]);
unused.forEach(img => console.log(' - ' + img));
