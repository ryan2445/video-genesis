export type IconsId =
  | "account-circle"
  | "account"
  | "check-circle"
  | "cog-outline"
  | "delete"
  | "pencil-outline"
  | "play"
  | "playlist-play"
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
  | "Play"
  | "PlaylistPlay"
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
  Play = "play",
  PlaylistPlay = "playlist-play",
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
  [Icons.Play]: "61703",
  [Icons.PlaylistPlay]: "61704",
  [Icons.PlaylistPlus]: "61705",
  [Icons.Video]: "61706",
  [Icons.WifiCancel]: "61707",
  [Icons.WifiCheck]: "61708",
};
