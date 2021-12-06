export type IconsId =
  | "check-circle"
  | "video";

export type IconsKey =
  | "CheckCircle"
  | "Video";

export enum Icons {
  CheckCircle = "check-circle",
  Video = "video",
}

export const ICONS_CODEPOINTS: { [key in Icons]: string } = {
  [Icons.CheckCircle]: "61697",
  [Icons.Video]: "61698",
};
