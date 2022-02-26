export type IconsId =
  | "account-circle"
  | "account"
  | "check-circle"
  | "cog-outline"
  | "video";

export type IconsKey =
  | "AccountCircle"
  | "Account"
  | "CheckCircle"
  | "CogOutline"
  | "Video";

export enum Icons {
  AccountCircle = "account-circle",
  Account = "account",
  CheckCircle = "check-circle",
  CogOutline = "cog-outline",
  Video = "video",
}

export const ICONS_CODEPOINTS: { [key in Icons]: string } = {
  [Icons.AccountCircle]: "61697",
  [Icons.Account]: "61698",
  [Icons.CheckCircle]: "61699",
  [Icons.CogOutline]: "61700",
  [Icons.Video]: "61701",
};
