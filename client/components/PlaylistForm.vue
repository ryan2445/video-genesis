<template>
  <div
    :style="'min-width:' + (minWidth || 560) + 'px;'"
    class="pt-2 pb-3 px-3 bg-white"
  >
    <v-form v-model="valid">
      <v-text-field
        v-model="title"
        :rules="titleRules"
        label="Playlist title*"
        required
        color="#A13440"
      >
      </v-text-field>
      <v-textarea
        v-model="description"
        :rules="descriptionRules"
        label="Playlist description"
        color="#A13440"
      >
      </v-textarea>

      <v-checkbox
        label="Make private"
        v-model="isPrivate"
        :rules="isPrivateRules"
        color="#A13440"
      >
      </v-checkbox>
      <div class="flex w-full justify-end">
        <v-btn class="mx-1" text @click="onCancel"> Cancel </v-btn>
        <v-btn
          class="mx-1 white--text"
          :disabled="!valid"
          color="#A13440"
          @click="onSubmit"
        >
          Create
        </v-btn>
      </div>
    </v-form>
  </div>
</template>

<script>
export default {
  name: "PlaylistForm",
  props: {
    minWidth: {
      type: Number | String,
      required: false,
    },
    video: {
      type: Object,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      valid: false,

      title: "",
      titleRules: [
        (v) => !!v || "Title is required",
        (v) => v.length <= 250 || "Title must be less than 250 characters",
      ],
      description: "",
      descriptionRules: [
        (v) =>
          v.length <= 1000 || "Description must be less than 1000 characters",
      ],

      isPrivate: false,
      isPrivateRules: [(v) => v === true || v === false || "Must be a boolean"],
    };
  },
  methods: {
    async onSubmit() {
      const payload = {
        playlistTitle: this.title,
        description: this.description,
        isPrivate: this.isPrivate,
      };

      if (this.video) {
        payload["video"] = this.video;
      }

      const response = await this.$store.dispatch(
        "playlists/playlistsPost",
        payload
      );

      if (!response) return;

      this.$emit("close");
    },
    onCancel() {
      this.$emit("close");
    },
  },
};
</script>
