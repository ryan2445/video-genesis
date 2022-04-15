<template>
  <div class="mt-3">
    <v-row>
      <v-col :cols="!!playlist && playlistLoaded ? '8' : '12'">
        <template v-if="!loading">
          <video-container
            :video="video"
            :audio="videoAudio"
            :start-time="startTime"
            :video-data="videoData"
            :autoplay="!!playlist"
            @video:ended="onVideoEnded"
          >
          </video-container>
        </template>
        <div v-if="!loading">
          <video-player-comment-list :video="video" />
        </div>
      </v-col>
      <v-col v-if="playlist && playlistLoaded" cols="4">
        <playlist-player
          :playlist="playlist"
          :index="index"
          :video="video"
          :replay="replay"
          @video:update="onPlaylistVideoUpdate"
          @shuffle="handleShuffle"
          @replay-pressed="replay = !replay"
        >
        </playlist-player>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "VideoPage",
  layout: "dashboard",
  data() {
    return {
      BUCKET_URL:
        "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
      video: null,
      loading: true,
      pk: null,
      sk: null,
      startTime: null,

      playlistLoaded: false,
      listPK: null,
      listSK: null,
      index: 0,
      replay: false,
      isShuffled: false
    };
  },
  created() {
    this.$store.commit("app/setRoute", "");

  },
  computed: {
    ...mapGetters({
      user: "users/rootUser",
      playlist: "playlists/selected_playlist"
    }),
    videoData() {
      // If the video is not loaded, return null
      if (!this.video || !this.video.videoData) {
        return null;
      }

      const data = this.video.videoData.map((data) => {
        return {
          type: "video/mp4",
          src: `${this.BUCKET_URL}/${this.video.videoKey}/${data.baseURL}`,
          label: `${data.width}`,
          res: data.width,
        };
      });

      return data;
    },
    videoAudio() {
      if (!this.video || !this.BUCKET_URL) {
        return null;
      }

      return `${this.BUCKET_URL}/${this.video.videoKey}/${this.video.videoKey}.mp4`;
    }
  },
  async mounted() {
    this.getQueryParamsAndSetKeys();

    if (this.listPK && this.listSK) {
      await this.getPlaylist();
    }

    await this.getAndSetVideo();

    const playlistString = localStorage.getItem('vg-playlist-shuffle')

    if (this.isShuffled && !!playlistString) {
      const savedPlaylist = JSON.parse(playlistString)

      this.$store.commit('playlists/selectedPlaylistSet', savedPlaylist)
    }

    this.loading = false;
  },
  methods: {
    async getPlaylist() {
      const playlistPK = this.listPK;
      const playlistSK = this.listSK;

      const params = {
        pk: playlistPK,
        sk: playlistSK,
      };

      const playlist = await this.$store.dispatch(
        "playlists/playlistGet",
        params
      );

      this.$store.commit('playlists/selectedPlaylistSet', playlist);

      this.playlistLoaded = true;
    },
    getQueryParamsAndSetKeys() {
      const path = this.$route.fullPath.replace("/videos/", "");
      const params = new URLSearchParams(path);

      // If the sk is not provided, error
      if (!params.has("sk")) {
        console.error("sort key not provided");
        return;
      }

      const pk = params.has("pk")
        ? params.get("pk")
        : this.$store.getters("users/rootUser").id;

      const sk = params.get("sk");

      const time = params.get("time");

      const listPK = params.has("listPK") ? params.get("listPK") : null;
      const listSK = params.has("listSK") ? params.get("listSK") : null;

      const index = params.has("index") ? params.get("index") : 0;

      const replay = params.has("replay");

      const shuffle = params.has('shuffle') ? params.get('shuffle') : 0

      this.pk = pk;
      this.sk = sk;
      this.listPK = listPK;
      this.listSK = listSK;
      this.startTime = time;
      this.index = Number(index);
      this.replay = Number(replay) ? true : false;
      this.isShuffled = Number(shuffle) ? true : false
    },
    async getAndSetVideo() {
      if (!this.pk || !this.sk) {
        console.error("Cannot get video without pk and sk");
        return;
      }

      const video = await this.$store.dispatch("videos/videoGet", {
        pk: this.pk,
        sk: this.sk,
      });

      this.video = video;
    },
    onPlaylistVideoUpdate({video, index}) {
      this.video = video;
      this.index = index;
      this.startTime = 0;
    },
    onVideoEnded() {
      // If the playlist does not exist, return
      if (!this.playlist || !this.playlistLoaded) return;

      const isLastPlaylistVideo = this.index >= this.playlist.videos.length - 1;

      if (!isLastPlaylistVideo || (isLastPlaylistVideo && this.replay)) {
        const idx = isLastPlaylistVideo ? 0 : this.index + 1;
        const { videoPK, videoSK } = this.playlist.videos[idx];
        const { pk, sk } = this.playlist;

        const url = `/videos/pk=${videoPK}&sk=${videoSK}&listPK=${pk}&listSK=${sk}&index=${idx}&replay=${this.replay ? 1 : 0}&shuffle=${this.isShuffled ? 1 : 0}`;

        this.$router.push(url);

        this.index = idx;
        this.video = this.playlist.videos[idx].video;
      }
    },
    handleShuffle() {
      const idx = this.playlist.videos
        .findIndex(pItem => 
          pItem.videoPK === this.video.pk && pItem.videoSK === this.video.sk
        )

      if (idx !== -1) {
        this.index = idx;
        this.isShuffled = true;
      }
      else {
        console.error('ERROR: handleShuffle() video loc unknown')
      }
    }
  },
};
</script>

<style></style>
