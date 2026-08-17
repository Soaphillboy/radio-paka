import React from "react";
import {
  AbsoluteFill,
  Img,
  OffthreadVideo,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { theme } from "./theme";

// Burn-in titri EHR parauga stilā (2026-07-23 "autocaptions ehr paraugs.mov"):
// frāzes rādās PĀROS — pirmā rinda SemiBold, viegli pieklusināta, zem tās otrā rinda
// ExtraBold tīri baltā; pirmā paliek redzama, kamēr skan otrā. Rinda bez pāra (pēc
// garākas pauzes vai pēdējā) ir uzreiz treknā. Rinda ielido VESELA ar ātru fade sava
// pirmā vārda brīdī (ne pa vārdam), pirmā rinda pāri neatceļ — jaunā pievienojas zem tās.
// Visi vārdi vienā izmērā (big atzīme tiek pieņemta, bet vairs nemaina izmēru).
// ==akcents== zīmola krāsā (accentColor prop) ar POP; ~~ig~~ ar IG gradientu pa burtiem.
// video="" nozīmē caurspīdīgu fonu (alpha overlay montāžai).
// title / titleBehind + cutout: intro virsraksti pa virsu vai aiz galvas izgriezuma.
// Izmēriem (FS 56, left 120, width 840) jāsakrīt ar make_captions.py aplēsēm.
// Props ģenerē caption_render.py.
export type CapWord = { t: number; text: string; big?: boolean; accent?: boolean; ig?: boolean };
export type CapPhrase = { start: number; end: number; words: CapWord[] };
export type CapTitle = { rows: CapWord[][]; until: number; from?: number; y: number; size: number; color?: string; keepPhrases?: boolean };
export type WordCaptionsProps = {
  video: string; // ceļš public/ iekšienē; "" = caurspīdīgs
  phrases: CapPhrase[];
  captionY: number; // pāra PIRMĀS rindas centra Y (1080x1920 logiskajā telpā)
  durationSec: number; // garums; Root calculateMetadata no tā rēķina kadrus
  accentColor?: string; // ==vārds== akcenta krāsa (no config.json), noklusēti oranžs
  title?: CapTitle | null;
  title2?: CapTitle | null; // otrā title fāze
  titleBehind?: CapTitle | null;
  cutout?: string | null; // public/ ceļš; galvas izgriezums virs titleBehind
  bgStill?: string | null; // public/ ceļš; fona kadrs preview pozicionēšanai
};

const FS = 56; // rindas fontSize — paraugā abas rindas vienā izmērā (~55px 1080 telpā)
const ACCENT_FS = 62; // akcenta/IG vārds nedaudz lielāks par pārējiem
const ROW_FADE_F = 5; // rindas fade-in garums kadros (paraugā ~0.2 s)
const PAIR_GAP = 1.0; // s: ja rinda sākas vēlāk par šo pēc iepriekšējās pēdējā vārda, sākas jauns pāris
const DIM = 0.85; // pāra pirmās (SemiBold) rindas opacity
const ROW_LH = 1.12;
const LETTER_D = 0.05; // IG akcenta burtu stagger (s)
// Parauga ēna: plāna tumša maliņa cieši ap burtiem ("outline" iespaids) + neliela mīksta ēna
const SHADOW = "0 2px 2px rgba(0,0,0,.55), 0 4px 10px rgba(0,0,0,.35), 0 10px 26px rgba(0,0,0,.28)";

const TitleBlock: React.FC<{ title: CapTitle; fade: (wt: number) => number; fallback: string }> = ({ title, fade, fallback }) => (
  <div
    style={{
      position: "absolute",
      top: title.y,
      left: 0,
      width: 1080,
      textAlign: "center",
      fontFamily: theme.fontFamily,
      fontWeight: theme.weight.black,
      color: title.color ?? fallback,
    }}
  >
    {title.rows.map((row, ri) => (
      <div key={ri} style={{ fontSize: title.size, lineHeight: 1.04, letterSpacing: 1 }}>
        {row.map((w, wi) => (
          <span
            key={wi}
            style={{
              display: "inline-block",
              opacity: fade(w.t),
              marginRight: wi < row.length - 1 ? 0.28 * title.size : 0,
              textShadow: "0 4px 14px rgba(0,0,0,.55), 0 0 40px rgba(0,0,0,.35)",
            }}
          >
            {w.text}
          </span>
        ))}
      </div>
    ))}
  </div>
);

export const WordCaptions: React.FC<WordCaptionsProps> = ({
  video, phrases, captionY, accentColor, title, title2, titleBehind, cutout, bgStill,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const accent = accentColor ?? theme.color.orange;

  // keepPhrases: title rāda paralēli parastajiem titriem
  const untilOf = (b?: CapTitle | null) => (b && !b.keepPhrases ? b.until : 0);
  const untilMax = Math.max(untilOf(title), untilOf(title2), untilOf(titleBehind));
  const inTitle = t < untilMax;
  const active = (b?: CapTitle | null) => b != null && t >= (b.from ?? 0) && t < b.until;
  const fade = (wt: number) =>
    interpolate((t - wt) * fps, [0, ROW_FADE_F], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const pop = (wt: number) =>
    spring({ fps, frame: Math.max(0, (t - wt) * fps), config: { damping: 9, stiffness: 170, mass: 0.6 } });

  // Frāžu pāri: rinda pieķeras iepriekšējai, ja sākas ≤PAIR_GAP pēc tās pēdējā vārda
  // (garāka pauze vai jau pilns pāris => jauns pāris). Pēdējā rinda pārī ir treknā.
  const pairs: number[][] = [];
  phrases.forEach((p, i) => {
    const last = pairs[pairs.length - 1];
    if (last && last.length === 1) {
      const prev = phrases[last[0]];
      const prevW = prev.words[prev.words.length - 1];
      if (prevW && p.start - prevW.t <= PAIR_GAP) {
        last.push(i);
        return;
      }
    }
    pairs.push([i]);
  });
  // Pāris redzams no pirmās rindas sākuma līdz pēdējās beigām; rinda parādās no sava sākuma
  const pair = inTitle
    ? undefined
    : pairs.find((rs) => t >= phrases[rs[0]].start && t < phrases[rs[rs.length - 1]].end);

  return (
    <AbsoluteFill style={{ background: video ? "#000" : "transparent" }}>
      {video ? (
        <OffthreadVideo src={staticFile(video)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      ) : bgStill ? (
        <Img src={staticFile(bgStill)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      ) : null}
      {active(titleBehind) ? <TitleBlock title={titleBehind!} fade={fade} fallback={accent} /> : null}
      {inTitle && cutout ? (
        <Img src={staticFile(cutout)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" }} />
      ) : null}
      {active(title) ? <TitleBlock title={title!} fade={fade} fallback={accent} /> : null}
      {active(title2) ? <TitleBlock title={title2!} fade={fade} fallback={accent} /> : null}
      {pair ? (
        <div
          style={{
            position: "absolute",
            // pirmās rindas centrs vienmēr captionY; nākamā rinda pievienojas ZEM tās
            top: captionY - (FS * ROW_LH) / 2,
            left: 120,
            width: 840,
          }}
        >
          {pair.map((pi, ri) => {
            const row = phrases[pi];
            if (t < row.start) return null;
            const bold = ri === pair.length - 1;
            return (
              <div
                key={pi}
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  justifyContent: "center",
                  alignItems: "baseline",
                  columnGap: 15,
                  rowGap: 4,
                  lineHeight: ROW_LH,
                  textAlign: "center",
                  fontFamily: theme.fontFamily,
                  color: theme.color.white,
                  opacity: fade(row.start) * (bold ? 1 : DIM),
                }}
              >
                {row.words.map((w, i) =>
                  w.ig ? (
                    // IG gradienta vārds: burti uzlec PA VIENAM (stagger LETTER_D), gradients
                    // stiepjas pāri visam vārdam (backgroundSize/Position nobīde pa burtiem);
                    // ēna caur drop-shadow uz wrappera (textShadow spīdētu cauri caurspīdīgajiem glifiem)
                    <span
                      key={i}
                      style={{
                        display: "inline-block",
                        fontSize: ACCENT_FS,
                        fontWeight: theme.weight.black,
                        whiteSpace: "pre",
                        filter: "drop-shadow(0 2px 3px rgba(0,0,0,.5)) drop-shadow(0 6px 14px rgba(0,0,0,.3))",
                      }}
                    >
                      {[...w.text].map((ch, ci, arr) => {
                        const p = pop(w.t + ci * LETTER_D);
                        return (
                          <span
                            key={ci}
                            style={{
                              display: "inline-block",
                              backgroundImage: "linear-gradient(95deg,#F58529 0%,#E1306C 55%,#C032C8 100%)",
                              backgroundSize: `${arr.length * 100}% 100%`,
                              backgroundPosition: `${arr.length > 1 ? (ci / (arr.length - 1)) * 100 : 0}% 0%`,
                              WebkitBackgroundClip: "text",
                              backgroundClip: "text",
                              color: "transparent",
                              opacity: interpolate(p, [0, 0.35], [0, 1], { extrapolateRight: "clamp" }),
                              transform: `scale(${p})`,
                              transformOrigin: "center bottom",
                            }}
                          >
                            {ch}
                          </span>
                        );
                      })}
                    </span>
                  ) : (
                    <span
                      key={i}
                      style={{
                        display: "inline-block",
                        fontSize: w.accent ? ACCENT_FS : FS,
                        color: w.accent ? accent : theme.color.white,
                        fontWeight: w.accent
                          ? theme.weight.black
                          : bold
                            ? theme.weight.extrabold
                            : theme.weight.semibold,
                        opacity: w.accent ? interpolate(pop(w.t), [0, 0.35], [0, 1], { extrapolateRight: "clamp" }) : 1,
                        transform: w.accent ? `scale(${pop(w.t)})` : undefined,
                        transformOrigin: "center bottom",
                        textShadow: SHADOW,
                      }}
                    >
                      {w.text}
                    </span>
                  )
                )}
              </div>
            );
          })}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
