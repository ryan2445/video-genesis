export type IconsId =
  | "video";

export type IconsKey =
  | "Video";

export enum Icons {
  Video = "video",
}

export const ICONS_CODEPOINTS: { [key in Icons]: string } = {
  [Icons.Video]: "61697",
};
