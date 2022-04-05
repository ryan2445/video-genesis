export type IconsId =
  | "account-circle"
  | "account"
  | "check-circle"
  | "cog-outline"
  | "delete"
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
  | "Delete"
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
  Delete = "delete",
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
  [Icons.Delete]: "61701",
  [Icons.PencilOutline]: "61702",
  [Icons.PlaylistPlus]: "61703",
  [Icons.Video]: "61704",
  [Icons.WifiCancel]: "61705",
  [Icons.WifiCheck]: "61706",
};
