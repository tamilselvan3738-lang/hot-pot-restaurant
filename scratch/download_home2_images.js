const fs = require('fs');
const path = require('path');
const https = require('https');

const IMAGES_DIR = path.join(__dirname, '..', 'images');

const downloads = [
  {
    name: 'home2-hero-cauldron-flame.jpg',
    url: 'https://upload.wikimedia.org/wikipedia/commons/2/2f/Chongqing.Original_Sichuan_hotpot_base.jpg'
  },
  {
    name: 'home2-first-boil-bubbles.jpg',
    url: 'https://upload.wikimedia.org/wikipedia/commons/f/fb/Shabu_Shabu_photo_Don_Ramey_Logan.jpg'
  },
  {
    name: 'home2-flavour-sensory-macro.jpg',
    url: 'https://upload.wikimedia.org/wikipedia/commons/e/e7/Spices_for_hot_pots.jpg'
  },
  {
    name: 'home2-overhead-shared-table.jpg',
    url: 'https://upload.wikimedia.org/wikipedia/commons/3/39/Hot_Pot_at_Chinese_Mongolian_Restaurant_in_Zhongshan.jpg'
  },
  {
    name: 'home2-table-craft-details.jpg',
    url: 'https://upload.wikimedia.org/wikipedia/commons/1/1e/Special_foods_%26_cuisines_in_Chongqing_-_Family_Dinner_2nd.jpg'
  },
  {
    name: 'home2-cinematic-grand-moment.jpg',
    url: 'https://upload.wikimedia.org/wikipedia/commons/0/0a/Yuanyang_Chongqing_Hotpot_Box_Hill.jpg'
  }
];

function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(dest);
    const options = {
      headers: {
        'User-Agent': 'HotPotApp/1.0 (info@hotpot.com)'
      }
    };

    function get(currentUrl) {
      https.get(currentUrl, options, res => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          get(res.headers.location);
          return;
        }
        if (res.statusCode !== 200) {
          reject(new Error(`Failed to download ${currentUrl}: HTTP ${res.statusCode}`));
          return;
        }
        res.pipe(file);
        file.on('finish', () => {
          file.close(resolve);
        });
      }).on('error', err => {
        fs.unlink(dest, () => reject(err));
      });
    }

    get(url);
  });
}

async function main() {
  if (!fs.existsSync(IMAGES_DIR)) {
    fs.mkdirSync(IMAGES_DIR, { recursive: true });
  }

  for (const item of downloads) {
    const dest = path.join(IMAGES_DIR, item.name);
    console.log(`Downloading ${item.name}...`);
    try {
      await downloadFile(item.url, dest);
      const stat = fs.statSync(dest);
      console.log(`✓ Saved ${item.name} (${Math.round(stat.size / 1024)} KB)`);
    } catch (err) {
      console.error(`✗ Error downloading ${item.name}:`, err.message);
    }
  }
}

main();
