#!/usr/bin/env python3
"""Resize + recompress localised assets, rename to the true extension, rewrite HTML refs."""
import os, glob, sys, shutil
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'clarks-mockups')
ASSETS = os.path.join(OUT, 'assets')
MAXW = 1600

def shrink_gif(path, maxw=460):
    """Re-encode an animated GIF smaller: halve the frames, cap the width."""
    import subprocess, tempfile
    out = tempfile.mktemp(suffix='.gif')
    for fps, colors, w in ((12, 128, maxw), (10, 96, 380), (8, 64, 320)):
        vf = ("fps=%d,scale=%d:-1:flags=lanczos,split[a][b];"
              "[a]palettegen=max_colors=%d[p];[b][p]paletteuse=dither=bayer" % (fps, w, colors))
        r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', path, '-vf', vf, out],
                           capture_output=True)
        if r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) < os.path.getsize(path) * 0.7:
            shutil.move(out, path)
            return


def main():
    renames = {}
    for f in sorted(glob.glob(os.path.join(ASSETS, '*'))):
        base = os.path.basename(f)
        if base.endswith('.mp4'):
            continue
        try:
            im = Image.open(f)
        except Exception:
            continue
        if getattr(im, 'is_animated', False):
            shrink_gif(f)
            continue
        w, h = im.size
        if w > MAXW:
            im = im.resize((MAXW, int(h * MAXW / w)), Image.LANCZOS)
        has_alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
        stem = os.path.splitext(base)[0]
        if has_alpha and (im.size[0] * im.size[1] < 400_000):
            # keep transparency (logos, badges) so CSS filters behave
            im = im.convert('RGBA')
            im.save(os.path.join(ASSETS, stem + '.png'), 'PNG', optimize=True)
            if base != stem + '.png':
                os.remove(f); renames[base] = stem + '.png'
            continue
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA')
            bg = Image.new('RGB', im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert('RGB')
        new = stem + '.jpg'
        im.save(os.path.join(ASSETS, new), 'JPEG', quality=80, optimize=True, progressive=True)
        if new != base:
            os.remove(f)
            renames[base] = new

    for p in glob.glob(os.path.join(OUT, '*.html')):
        s = open(p, encoding='utf-8').read()
        for old, new in renames.items():
            s = s.replace('assets/' + old, 'assets/' + new)
        open(p, 'w', encoding='utf-8').write(s)
    total = sum(os.path.getsize(f) for f in glob.glob(os.path.join(ASSETS, '*')))
    print('renamed %d, assets now %.1f MB' % (len(renames), total / 1e6))

if __name__ == '__main__':
    main()
