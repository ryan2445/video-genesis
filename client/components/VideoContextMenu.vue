<template>
  <v-list flat dense>
    <v-list-item
      v-for="(item, i) in listItems"
      :key="`context-menu-item-${i}`"
      @click="item.action()"
      class="contextMenuItem"
      dense
    >
      <v-list-item-content>
        <v-list-item-title>
          <span class="text-gray-100">
            {{ item.title }}
          </span>
        </v-list-item-title>
      </v-list-item-content>
      <v-list-item-avatar size="30">
        <v-icon v-if="!!item.model && $data[item.model]" color="white">
          icon-check-circle
        </v-icon>
      </v-list-item-avatar>
    </v-list-item>
  </v-list>
</template>

<script>
export default {
  name: "VideoContextMenu",
  props: {
    video: {
      type: Object,
      required: true,
    },
    videosShown: {
      type: Number,
      required: false,
      default: 1,
    },
  },
  data() {
    return {
      displayDefault: true,
      displayLR: false,
      displayHR: false,
      columnLayout: true,
    };
  },
  computed: {
    listItems() {
      const items = [
        {
          type: "button",
          title: "stats",
          action: this.showStats,
        },
      ];

      if (!!this.video.lrBaseURL && !!this.video.hrBaseURL) {
        items.push(
          {
            type: "switch",
            title: "show default video",
            action: this.showDefault,
            model: "displayDefault",
          },
          {
            type: "switch",
            title: "show 4x downsampled",
            action: this.showLR,
            model: "displayLR",
          },
          {
            type: "switch",
            title: "show super resolution",
            action: this.showHR,
            model: "displayHR",
          },
          {
            type: "button",
            title: "sync videos",
            action: this.syncVideos,
          },
          {
            type: "button",
            title: `stack videos ${
              this.columnLayout ? "vertically" : "horizontally"
            }`,
            action: this.toggleLayout,
          }
        );
      }

      return items;
    },
  },
  methods: {
    showStats() {
      this.$emit("show:stats");
      this.$emit("close");
    },
    showLR() {
      if (this.videosShown == 1 && this.displayLR == true) return;

      this.displayLR = !this.displayLR;
      this.$emit("show:lr", this.displayLR);
    },
    showHR() {
      if (this.videosShown == 1 && this.displayHR == true) return;

      this.displayHR = !this.displayHR;
      this.$emit("show:hr", this.displayHR);
    },
    syncVideos() {
      this.$emit("sync");
    },
    toggleLayout() {
      this.columnLayout = !this.columnLayout;
      this.$emit("toggle:layout", this.columnLayout);
    },
    showDefault() {
      if (this.videosShown == 1 && this.displayDefault == true) return;
      this.displayDefault = !this.displayDefault;
      this.$emit("show:default", this.displayDefault);
    },
  },
};
</script>

<style scoped>
.contextMenuItem {
  background: none !important;
}
</style>
