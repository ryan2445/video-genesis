<template>
  <div class="relative">
    <div class="absolute -bottom-7 left-64">
      <h3>
        <strong>
          {{ user | userDisplayName }}
        </strong>
      </h3>
    </div>
    <!-- This is the cover image for the banner -->
    <v-hover v-slot="{ hover }" :open-delay="100">
      <div v-if="bannerSrc" class="w-full h-52 relative">
        <img class="w-full h-full object-cover" :src="bannerSrc" alt="banner" />
        <v-fade-transition>
          <v-btn
            v-if="isRootUser && (hover || bannerPictureLoading)"
            icon
            absolute
            right
            outlined
            small
            elevation="4"
            style="bottom: 6px; backdrop-filter: blur(8px)"
            @click="onBannerEdit"
            :loading="bannerPictureLoading"
            :disabled="bannerPictureLoading"
          >
            <v-icon small>icon-pencil-outline</v-icon>
          </v-btn>
        </v-fade-transition>
        <v-file-input
          class="absolute"
          ref="bannerEditFile"
          dense
          flat
          hide-details
          hide-input
          hide-spin-buttons
          :loader-height="0"
          prepend-icon
          accept="image/png, image/jpeg, image/bmp"
          :rules="fileRules"
          @change="onBannerChange"
        />
      </div>
    </v-hover>
    <v-hover v-slot="{ hover }" :open-delay="100">
      <div
        v-if="userProfilePic"
        class="-bottom-16 left-14 absolute w-44 h-44"
      >
        <img
          class="w-full h-full object-cover rounded-full"
          :src="userProfilePic"
          alt="avatar"
          style="border: solid 2px #e1e1e1"
        />
        <v-fade-transition>
          <v-btn
            v-if="isRootUser && (hover || profilePictureLoading)"
            icon
            absolute
            outlined
            small
            elevation="4"
            style="bottom: 12px; right: 22px; backdrop-filter: blur(8px)"
            @click="onProfilePictureEdit"
            :disabled="profilePictureLoading"
            :loading="profilePictureLoading"
          >
            <v-icon small>icon-pencil-outline</v-icon>
          </v-btn>
        </v-fade-transition>

        <v-file-input
          class="absolute"
          ref="profileEditFile"
          dense
          flat
          hide-details
          hide-input
          hide-spin-buttons
          :loader-height="0"
          prepend-icon
          accept="image/png, image/jpeg, image/bmp"
          :rules="fileRules"
          @change="onProfilePictureChange"
        />
      </div>
    </v-hover>
  </div>
</template>

<script>
import s3 from "../mixins/s3";
import { mapGetters } from "vuex";
export default {
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  mixins: [s3],
  data() {
    return {
      fileRules: [
        (value) =>
          !value || value < 25000000 || "Image should be less than 25 MB",
      ],
      profilePictureLoading: false,
      bannerPictureLoading: false,
    };
  },
  computed: {
    ...mapGetters({ rootUser: "users/rootUser" }),
    userProfilePic() {
      // If the user does not exist, return null
      if (!this.user) return null;

      return (
        this.user.profilePicKey ||
        "https://www.unr.edu/main/images/divisions/president/marketing-communications/brand/brand-athletics-2.png"
      );
    },
    bannerSrc() {
      // If the user does not exist, return null
      if (!this.user) return null;

      return (
        this.user.coverPicKey ||
        "https://www.unr.edu/main/images/top-6/visit/components/campus-360.jpg"
      );
    },
    isRootUser() {
      if (!this.user) return null;

      return this.user.username == this.rootUser.username;
    },
  },
  methods: {
    onProfilePictureEdit() {
      if (!this.isRootUser) return;

      const el = this.$refs.profileEditFile?.$el;
      if (!el) return;

      const file_button = el.children[0]?.children[0]?.children[0];
      if (!file_button) return;

      file_button.click();
    },
    onBannerEdit() {
      if (!this.isRootUser) return;

      const el = this.$refs.bannerEditFile?.$el;
      if (!el) return;

      const file_button = el.children[0]?.children[0]?.children[0];
      if (!file_button) return;

      file_button.click();
    },
    async onProfilePictureChange(file) {
      if (!this.isRootUser || !file || !file.type) return;

      this.profilePictureLoading = true;

      try {
        const bucket = "videogenesis-profilepics";

        // If the user has an existing profile picture, delete it
        if (this.user.profilePicKey) {
          const delete_key = this.key_from_string(this.user.profilePicKey);

          this.s3_delete(bucket, delete_key);
        }

        // Construct the put key from the file
        const put_key = this.key_from_file(file);

        // Upload the profile picture to s3
        const profile_pic_key = await this.s3_put(bucket, put_key, file);

        // Update the root user locally
        this.$store.commit("users/rootUserSet", {
          ...this.user,
          profilePicKey: profile_pic_key,
        });

        // Update the users on the server
        await this.$store.dispatch("users/userPut", {
          profilePicKey: profile_pic_key,
        });
      } catch (error) {
        console.error(error);
      }

      this.profilePictureLoading = false;
    },
    async onBannerChange(file) {
      if (!this.isRootUser || !file || !file.type) return;

      this.bannerPictureLoading = true;

      try {
        const bucket = "videogenesis-profilepics";

        //  Delete old banner
        if (this.bannerSrc) {
          const delete_key = this.key_from_string(this.bannerSrc);

          await this.s3_delete(bucket, delete_key);
        }

        const put_key = this.key_from_file(file);

        const banner_key = await this.s3_put(bucket, put_key, file);

        this.$store.commit("users/rootUserSet", {
          ...this.user,
          coverPicKey: banner_key,
        });

        await this.$store.dispatch("users/userPut", {
          coverPicKey: banner_key,
        });
      } catch (error) {
        console.error(error);
      }

      this.bannerPictureLoading = false;
    },
  },
};
</script>
