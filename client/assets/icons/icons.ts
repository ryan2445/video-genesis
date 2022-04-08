export type IconsId =
  | "account-circle"
  | "account"
  | "check-circle"
  | "chevron-right"
  | "close"
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
  | "Close"
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
  Close = "close",
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
  [Icons.Close]: "61701",
  [Icons.CogOutline]: "61702",
  [Icons.Delete]: "61703",
  [Icons.PencilOutline]: "61704",
  [Icons.Play]: "61705",
  [Icons.PlaylistPlay]: "61706",
  [Icons.PlaylistPlus]: "61707",
  [Icons.Video]: "61708",
  [Icons.WifiCancel]: "61709",
  [Icons.WifiCheck]: "61710",
};
