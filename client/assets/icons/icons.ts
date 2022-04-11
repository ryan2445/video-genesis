export type IconsId =
  | "account-circle"
  | "account"
  | "check-circle"
  | "chevron-right"
  | "close"
  | "cog-outline"
  | "delete"
  | "lightning-bolt-circle"
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
  | "LightningBoltCircle"
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
  LightningBoltCircle = "lightning-bolt-circle",
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
  [Icons.LightningBoltCircle]: "61704",
  [Icons.PencilOutline]: "61705",
  [Icons.Play]: "61706",
  [Icons.PlaylistPlay]: "61707",
  [Icons.PlaylistPlus]: "61708",
  [Icons.Video]: "61709",
  [Icons.WifiCancel]: "61710",
  [Icons.WifiCheck]: "61711",
};
