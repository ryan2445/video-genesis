<template>
  <div class="mt-3">
    <v-row>
      <v-col :cols="!!playlist ? '8' : '12'">
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
      <v-col cols="4">
        <playlist-player
          v-if="playlist"
          :playlist="playlist"
          :index="index"
          @video:update="onPlaylistVideoUpdate"
        >
        </playlist-player>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import VideoPlayerCommentList from "../../components/VideoPlayerCommentList.vue";
export default {
  components: { VideoPlayerCommentList },
  name: "VideoPage",
  layout: "dashboard",
  data() {
    return {
      bucket_url:
        "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
      video: null,
      loading: true,
      pk: null,
      sk: null,
      startTime: null,

      listPK: null,
      listSK: null,
      index: 0,
      playlist: null,
    };
  },
  created() {
    this.$store.commit("app/setRoute", "");
  },
  computed: {
    ...mapGetters({
      user: "users/rootUser",
    }),
    videoData() {
      // If the video is not loaded, return null
      if (!this.video || !this.video.videoData) {
        return null;
      }

      //this.$store.commit("app/setRoute", this.video.videoTitle);

      const data = this.video.videoData.map((data) => {
        return {
          type: "video/mp4",
          src: `${this.bucket_url}/${this.video.videoKey}/${data.baseURL}`,
          label: `${data.width}`,
          res: data.width,
        };
      });

      return data;
    },
    videoAudio() {
      if (!this.video || !this.bucket_url) {
        return null;
      }

      return `${this.bucket_url}/${this.video.videoKey}/${this.video.videoKey}.mp4`;
    },
  },
  async mounted() {
    this.getQueryParamsAndSetKeys();

    if (this.listPK && this.listSK) {
      await this.getPlaylist();
    }

    await this.getAndSetVideo();

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

      console.log('playlist', playlist)

      this.playlist = playlist;
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

      this.pk = pk;
      this.sk = sk;
      this.listPK = listPK;
      this.listSK = listSK;
      this.startTime = time;
      this.index = Number(index);
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
    onPlaylistVideoUpdate(video) {
      this.video = video;
      this.startTime = 0;
    },
    onVideoEnded() {
      // If the playlist does not exist, return
      if (!this.playlist) return;

      const isLastPlaylistVideo = this.index >= this.playlist.videos.length - 1;

      if (!isLastPlaylistVideo) {
        this.index = this.index + 1;
        this.video = this.playlist.videos[this.index].video;
        const url = `/videos/pk=${this.video.pk}&sk=${this.video.sk}&listPK=${this.playlist.pk}&listSK=${this.playlist.sk}&index=${this.index}`
        this.$router.push(url);
      }
    },
  },
};
</script>

<style></style>
