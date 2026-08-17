import React from "react";
import { Composition } from "remotion";
import { VIDEO } from "./theme";
import { WordCaptions } from "./WordCaptions";

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="WordCaptions"
      component={WordCaptions}
      durationInFrames={30}
      fps={VIDEO.fps}
      width={VIDEO.width}
      height={VIDEO.height}
      defaultProps={{ video: "", phrases: [], captionY: 1250, durationSec: 1, title: null }}
      calculateMetadata={({ props }) => ({
        durationInFrames: Math.max(1, Math.ceil((props as { durationSec: number }).durationSec * VIDEO.fps)),
      })}
    />
  </>
);
