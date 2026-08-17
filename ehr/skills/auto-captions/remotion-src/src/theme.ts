// EHR captions tēma: Montserrat fonts + krāsas. Akcenta krāsu parasti nemaina šeit,
// bet config.json laukā accentColor (caption_render.py to padod kā prop).
import { loadFont } from "@remotion/google-fonts/Montserrat";

// Tikai vajadzīgie svari; latin-ext dod latviešu diakritikas (ā č ē ģ ķ ļ ņ š ž),
// cyrillic vajadzīgs krievu saturam (piem. EHR Plus).
const { fontFamily } = loadFont("normal", {
  weights: ["600", "800", "900"],
  subsets: ["latin", "latin-ext", "cyrillic", "cyrillic-ext"],
});

export const theme = {
  fontFamily, // Montserrat
  color: {
    orange: "#F17E18", // akcenta noklusējums, ja config.json nav accentColor
    white: "#FFFFFF",
  },
  weight: {
    semibold: 600, // pāra pirmā (ievada) rinda
    extrabold: 800, // pāra pēdējā (treknā) rinda
    black: 900, // akcenti un virsraksti
  },
} as const;

export const VIDEO = { width: 1080, height: 1920, fps: 30 } as const;
