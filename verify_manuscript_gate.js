const fs = require('fs');
const path = require('path');

const repoRoot = path.resolve(__dirname);
const defaultPath = path.join(
  'uet_history', '3_publish', 'books', 'biology_psychology_economics',
  '01_biology', 'ch_drafts', 'UET_BOOK_CONTENT_DRAFTS.md'
);
const requested = process.argv[2] || process.env.UET_MANUSCRIPT_PATH || defaultPath;
const filePath = path.resolve(repoRoot, requested);
if (!filePath.startsWith(repoRoot + path.sep)) {
  console.error('FAILED: manuscript path must stay inside the repository.');
  process.exit(1);
}
if (!fs.existsSync(filePath)) {
  console.error('BLOCKED: local manuscript input is not present:', path.relative(repoRoot, filePath));
  console.error('Pass a repo-relative path as the first argument or set UET_MANUSCRIPT_PATH.');
  process.exit(2);
}
const content = fs.readFileSync(filePath, 'utf8');
const lines = content.split(/\r?\n/);
const minimumLines = Number(process.env.UET_MIN_LINES || 1);
const headingCount = lines.filter(line => /^#{1,6}\s+/.test(line)).length;
console.log('--- MANUSCRIPT INTEGRITY GATE ---');
console.log('Input:', path.relative(repoRoot, filePath));
console.log('Lines:', lines.length);
console.log('Headings:', headingCount);
if (content.includes('\0')) {
  console.error('FAILED: NUL byte found in manuscript text.');
  process.exit(1);
}
if (lines.length < minimumLines) {
  console.error('FAILED: line count is below UET_MIN_LINES:', minimumLines);
  process.exit(1);
}
if (headingCount === 0) {
  console.error('FAILED: manuscript has no headings.');
  process.exit(1);
}
console.log('PASSED: structural integrity checks completed.');
