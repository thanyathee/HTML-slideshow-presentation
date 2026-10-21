// Prints QR codes (SVG) for the contact slide as JSON
import QRCode from 'qrcode'
const urls = {
  scholarship: 'https://scholarship.tiscofoundation.org',
  website: 'https://www.tiscofoundation.org',
  facebook: 'https://www.facebook.com/tiscofoundation'
}
const out = {}
for (const [k, u] of Object.entries(urls)) out[k] = await QRCode.toString(u, { type: 'svg', margin: 1, errorCorrectionLevel: 'M', color: { dark: '#06133F', light: '#FFFFFF' } })
console.log(JSON.stringify(out))
