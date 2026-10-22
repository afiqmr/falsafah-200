# Design

Calm, warm and readable at night. The Arabic is the hero of every card; everything else
supports it.

## Themes

Two themes, switched from the header. Colours are CSS custom properties on `:root` (dark) and
`body[data-theme="light"]`; components use only the tokens.

| Token          | Dark      | Light     | Use                                         |
| -------------- | --------- | --------- | ------------------------------------------- |
| `--bg`         | `#121316` | `#FAF5EC` | Page                                        |
| `--surface`    | `#1E2026` | `#FFFDF9` | Cards                                       |
| `--surface-2`  | `#262932` | `#F7ECD6` | Inset panels, buttons                       |
| `--ink`        | `#DEDFE2` | `#10212B` | Text                                        |
| `--muted`      | `#9DA3AE` | `#5F6B6D` | Secondary text                              |
| `--gold`       | `#C9A85C` | `#FF7F50` | Primary action and active tab               |
| `--gold-cite`  | `#D4B46A` | `#0F766E` | Numbers, labels and references              |
| `--emerald`    | `#7CC4A4` | `#0F766E` | Ingat, correct, done                        |
| `--rose`       | `#D98C86` | `#B42318` | Belum ingat, wrong                          |
| `--bm`         | `#9DB4D6` | `#3B5B8C` | BM line in word by word                     |

Gred colours run from green (A+) through gold (B) to orange and red (C, D, G).

## Type

- Interface: **Noto Sans**, 400 to 800.
- Arabic: **Scheherazade New**, large (about 27 px on phones in Kaji), generous line height.
- Phones zoom the page to 90%, and text boxes stay at 16 px on screen so iPhone does not zoom in.

## Motif

A songket band is drawn in code in the theme colours:

- faint at the left and right of the page on wide screens, fading toward the content;
- behind the account menu;
- as the top and bottom bands of the share card.

The share card always uses the light theme, keeps fixed font sizes, and grows in height with the
ayat.

## Patterns

- **Mission bar**: streak, Kaji and Kuiz for today. Numbers turn green at the target.
- **Cards** have a coloured top edge, rounded corners and a soft shadow.
- **Buttons** are full pills for actions, outlined pills for options.
- **Celebrations** are short: a ribbon burst and a note that closes by itself.
- **Motion** uses the iOS curve (`cubic-bezier(.32,.72,0,1)`); respect reduced motion.
- **Words**: short, plain sentences in BM.
