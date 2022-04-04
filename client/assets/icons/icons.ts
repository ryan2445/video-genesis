export type IconsId =
  | "account-circle"
  | "account"
  | "check-circle"
  | "cog-outline"
  | "pencil-outline"
  | "playlist-plus"
  | "video"
  | "wifi-cancel"
  | "wifi-check";

export type IconsKey =
  | "AccountCircle"
  | "Account"
  | "CheckCircle"
  | "CogOutline"
  | "PencilOutline"
  | "PlaylistPlus"
  | "Video"
  | "WifiCancel"
  | "WifiCheck";

export enum Icons {
  AccountCircle = "account-circle",
  Account = "account",
  CheckCircle = "check-circle",
  CogOutline = "cog-outline",
  PencilOutline = "pencil-outline",
  PlaylistPlus = "playlist-plus",
  Video = "video",
  WifiCancel = "wifi-cancel",
  WifiCheck = "wifi-check",
}

export const ICONS_CODEPOINTS: { [key in Icons]: string } = {
  [Icons.AccountCircle]: "61697",
  [Icons.Account]: "61698",
  [Icons.CheckCircle]: "61699",
  [Icons.CogOutline]: "61700",
  [Icons.PencilOutline]: "61701",
  [Icons.PlaylistPlus]: "61702",
  [Icons.Video]: "61703",
  [Icons.WifiCancel]: "61704",
  [Icons.WifiCheck]: "61705",
};
