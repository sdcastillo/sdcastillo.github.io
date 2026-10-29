#!/usr/bin/env python3
"""Insert tip/pay buttons into Sam News homepage + articles. Idempotent."""

from __future__ import annotations

from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent

HOME_TIP = """
  <section id="support" class="tip-strip tip-strip--home" aria-labelledby="support-title">
    <div class="tip-inner">
      <p class="tip-kicker">Support</p>
      <h2 id="support-title">Tip the reporter</h2>
      <p class="tip-lede">If these briefings help, tip via X Money (preferred), Cash App, or PayPal.</p>
      <div class="tip-actions">
        <a class="tip-btn tip-btn--x" href="https://x.com/SamCast65215624" rel="noopener noreferrer" target="_blank">
          <span class="tip-btn-label">X Money</span>
          <span class="tip-btn-hint">Preferred · tip via X</span>
        </a>
        <a class="tip-btn tip-btn--cash" href="https://cash.app/$samiamcastillo" rel="noopener noreferrer" target="_blank">
          <span class="tip-btn-label">Cash App</span>
          <span class="tip-btn-hint">$samiamcastillo</span>
        </a>
        <a class="tip-btn tip-btn--paypal" href="mailto:castillo.sam.d@gmail.com">
          <span class="tip-btn-label">PayPal</span>
          <span class="tip-btn-hint">castillo.sam.d@gmail.com</span>
        </a>
      </div>
    </div>
  </section>

"""

ARTICLE_TIP = """
  <aside class="tip-strip tip-strip--article" aria-label="Tip the reporter">
    <div class="tip-inner tip-inner--compact">
      <p class="tip-compact-label">Tip · <span class="tip-preferred">X Money preferred</span></p>
      <div class="tip-actions tip-actions--compact">
        <a class="tip-btn tip-btn--x tip-btn--sm" href="https://x.com/SamCast65215624" rel="noopener noreferrer" target="_blank">X Money</a>
        <a class="tip-btn tip-btn--cash tip-btn--sm" href="https://cash.app/$samiamcastillo" rel="noopener noreferrer" target="_blank">Cash App</a>
        <a class="tip-btn tip-btn--paypal tip-btn--sm" href="mailto:castillo.sam.d@gmail.com" title="PayPal · castillo.sam.d@gmail.com">PayPal</a>
      </div>
      <p class="tip-email-note">PayPal: <a href="mailto:castillo.sam.d@gmail.com">castillo.sam.d@gmail.com</a></p>
    </div>
  </aside>

"""

FOOTER_MARK = '  <footer class="site-footer">'


def patch_home(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'id="support"' in text and "tip-strip--home" in text:
        return False
    if FOOTER_MARK not in text:
        raise SystemExit(f"footer marker missing in {path}")
    # Drop a prior half-applied strip if present
    if "tip-strip" in text and "tip-strip--home" not in text:
        pass
    path.write_text(text.replace(FOOTER_MARK, HOME_TIP + FOOTER_MARK, 1), encoding="utf-8")
    return True


def patch_article(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "tip-strip--article" in text:
        return False
    if FOOTER_MARK not in text:
        raise SystemExit(f"footer marker missing in {path}")
    path.write_text(text.replace(FOOTER_MARK, ARTICLE_TIP + FOOTER_MARK, 1), encoding="utf-8")
    return True


def main() -> None:
    home = SITE_ROOT / "index.html"
    changed = []
    if patch_home(home):
        changed.append(str(home.relative_to(SITE_ROOT)))
    for art in sorted((SITE_ROOT / "articles").glob("*.html")):
        if patch_article(art):
            changed.append(str(art.relative_to(SITE_ROOT)))
    print(f"patched {len(changed)} files")
    for c in changed[:5]:
        print(f"  {c}")
    if len(changed) > 5:
        print(f"  … and {len(changed) - 5} more")


if __name__ == "__main__":
    main()
