// news-image-20261122 entry for @desnutt-y: copies the finished front page
// (entry.png, drawn for Sunday, 22 November 2026) to the output directory.
// Node 22, standard library only, no network.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
