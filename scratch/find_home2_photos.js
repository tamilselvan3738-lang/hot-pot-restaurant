const https = require('https');

async function searchWiki(query, limit = 5) {
  const url = `https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=${encodeURIComponent(query)}&srnamespace=6&format=json&srlimit=${limit}`;
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'HotPotApp/1.0 (info@hotpot.com)' } }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json.query ? json.query.search : []);
        } catch(e) { reject(e); }
      });
    }).on('error', reject);
  });
}

async function getImageUrl(title) {
  const url = `https://commons.wikimedia.org/w/api.php?action=query&titles=${encodeURIComponent(title)}&prop=imageinfo&iiprop=url|size&format=json`;
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'HotPotApp/1.0 (info@hotpot.com)' } }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          const pages = json.query.pages;
          const pageId = Object.keys(pages)[0];
          resolve(pages[pageId].imageinfo ? pages[pageId].imageinfo[0] : null);
        } catch(e) { reject(e); }
      });
    }).on('error', reject);
  });
}

async function main() {
  const targets = [
    { section: 1, concept: 'Hero Cauldron', query: 'chongqing hot pot steam' },
    { section: 2, concept: 'First Boil Bubbles', query: 'shabu shabu broth' },
    { section: 3, concept: 'Sensory Flavour Macro', query: 'wagyu beef hot pot sliced' },
    { section: 4, concept: 'Overhead Table', query: 'hot pot meal dinner' },
    { section: 5, concept: 'Table Craft Details', query: 'chinese dining table setting restaurant' },
    { section: 6, concept: 'Cinematic Grand Moment', query: 'hot pot celebration banquet' }
  ];

  for (const t of targets) {
    console.log(`\n=================== Sec ${t.section}: ${t.concept} (${t.query}) ===================`);
    const results = await searchWiki(t.query, 6);
    for (const r of results) {
      if (r.title.endsWith('.jpg') || r.title.endsWith('.png')) {
        const info = await getImageUrl(r.title);
        if (info && info.width > 1200) {
          console.log(`- ${r.title} (${info.width}x${info.height})\n  ${info.url}`);
        }
      }
    }
  }
}

main().catch(console.error);
