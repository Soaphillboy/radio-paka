import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("png"); // png kadri saglabā alpha kanālu ProRes 4444 renderiem
Config.setConcurrency(1); // stabilitāte: novērš renderu karāšanos noslogotā sistēmā
Config.overrideWebpackConfig((c) => c);
