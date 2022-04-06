export type IconsId =
  | "account-circle"
  | "account"
  | "check-circle"
  | "chevron-right"
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
  | "ChevronRight"
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
  ChevronRight = "chevron-right",
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
  [Icons.ChevronRight]: "61700",
  [Icons.CogOutline]: "61701",
  [Icons.Delete]: "61702",
  [Icons.PencilOutline]: "61703",
  [Icons.Play]: "61704",
  [Icons.PlaylistPlay]: "61705",
  [Icons.PlaylistPlus]: "61706",
  [Icons.Video]: "61707",
  [Icons.WifiCancel]: "61708",
  [Icons.WifiCheck]: "61709",
};
