# Sum up 18 November 2026's world news in one image

A one-page newspaper front page, drawn programmatically (no AI-generated
faces or text, so nothing is garbled): `draw_news.py` renders the 1024x1024
PNG with Pillow, `main.py` copies it to `/output/entry.png`.

## Stories (all reported on Wednesday 18 November 2026)

1. **Shenzhen summit** — Trump lands in Shenzhen, greeted by Xi at the
   airport; the first-ever Trump–Xi–Putin trilateral is set for Thursday.
   Xi and Putin met for the 50th time earlier in the day.
2. **Gulf war widens** — US strikes a missile site on Qeshm Island; Iran
   fires drones at US bases in Bahrain and Kuwait; a ship is struck in the
   Strait of Hormuz.
3. **Kerch bridge** — A Ukrainian strike collapses part of the bridge to
   Crimea for a second day; traffic is halted.
4. **Measles** — The US loses its measles-free status: 5,400+ cases,
   10 deaths, the first loss in 26 years.
5. **Ebola** — The DR Congo outbreak more than doubles: 11,000+ cases,
   5,400 deaths, the UN says.
6. **Alaska** — Democrat Mary Peltola wins the Senate race; Democrats
   reach 56 seats, 56–44.

Footer: Cyclone Xavier (Category 5) hits the Cook Islands; a Russian
military plane crashes in Siberia, 19 dead; S&P 500 −1.03%, Brent $92.47.

Sources checked 18 Nov 2026: Reuters, AP via Outlook India / Times of
India, Horizon, One Turn.

## Run

```sh
python3 draw_news.py            # regenerate entry.png (needs Pillow)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see LICENSE.
