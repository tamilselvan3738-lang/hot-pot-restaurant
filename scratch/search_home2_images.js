const https = require('https');

async function searchWiki(query) {
  const url = `https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=${encodeURIComponent(query)}&srnamespace=6&format=json&srlimit=6`;
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'HotPotApp/1.0 (info@hotpot.com)' } }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json.query.search);
        } catch(e) {
          reject(e);
        }
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
          resolve(pages[pageId].imageinfo ? pages[pageId].imageinfo[0].url : null);
        } catch(e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

async function main() {
  const queries = [
    'hot pot steam boil',
    'shabu shabu boiling',
    'hot pot table overhead',
    'hot pot tableware spoon',
    'chinese hot pot restaurant dining'
  ];

  for (const q of queries) {
    console.log(`\n=== SEARCH: ${q} ===`);
    const results = await searchWiki(q);
    for (const r of results.slice(0, 3)) {
      const imgUrl = await getImageUrl(r.title);
      console.log(`- Title: ${r.title}\n  URL: ${imgUrl}`);
    }
  }
}

main().catch(console.error);
