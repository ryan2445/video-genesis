<template>
  <div class="relative">
    <!-- This is the cover image for the banner -->
    <v-hover v-slot="{ hover }" :open-delay="100">
      <div v-if="bannerSrc" class="w-full h-32 relative">
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
            style="bottom:6px; backdrop-filter: blur(8px);"
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
      <div v-if="userProfilePic" class="-bottom-16 left-14 absolute w-44 h-44">
        <img class="w-full h-full object-cover rounded-full" :src="userProfilePic" alt="avatar" />
        <v-fade-transition>
          <v-btn
            v-if="isRootUser && (hover || profilePictureLoading)"
            icon
            absolute
            outlined
            small
            elevation="4"
            style="bottom:12px; right:22px; backdrop-filter: blur(8px);"
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
import { nanoid } from "nanoid";
import { PutObjectCommand, DeleteObjectCommand } from "@aws-sdk/client-s3";
export default {
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      fileRules: [
        value => !value || value < 25000000 || 'Image should be less than 25 MB'
      ],
      profilePictureLoading: false,
      bannerPictureLoading: false
    }
  },
  computed: {
    userProfilePic() {
      // If the user does not exist, return null
      if (!this.user) return null;

      return this.user.profilePicKey || "https://www.unr.edu/main/images/divisions/president/marketing-communications/brand/brand-athletics-2.png";
    },
    bannerSrc() {
      // If the user does not exist, return null
      if (!this.user) return null;

      return this.user.coverPicKey || "https://www.unr.edu/main/images/top-6/visit/components/campus-360.jpg";
    },
    isRootUser() {
      if (!this.user) return null

      return this.user.pk == this.$store.getters['users/rootUser'].pk
    }
  },
  methods: {
    onProfilePictureEdit() {
      if (!this.isRootUser) return

      const el = this.$refs.profileEditFile?.$el
      if (!el) return

      const file_button = el.children[0]?.children[0]?.children[0]
      if (!file_button) return

      file_button.click()
    },
    onBannerEdit() {
      if (!this.isRootUser) return

      const el = this.$refs.bannerEditFile?.$el
      if (!el) return

      const file_button = el.children[0]?.children[0]?.children[0]
      if (!file_button) return

      file_button.click()
    },
    async onProfilePictureChange(file) {
      if (!this.isRootUser) return

      if (!file || !file.type) return

      const typeArr = file.type.split("/");
      this.profilePictureLoading = true
      

      try {
        const bucket = "videogenesis-profilepics"

        //  Delete old profile
        if (this.user.profilePicKey) {
          const urlArr = this.user.profilePicKey.split("/");
          const deleteKey = urlArr[urlArr.length - 1];

          const deletePayload = {
            Bucket: bucket,
            Key: deleteKey,
          };

          const deleteCommand = new DeleteObjectCommand(deletePayload);
          await this.$store.getters["auth/s3"].send(
            deleteCommand
          );
        }

        const putPayload = {
          Bucket: bucket,
          Key: nanoid() + `.${typeArr[typeArr.length - 1]}`,
          Body: file,
        };

        const putCommand = new PutObjectCommand(putPayload);
        const putResp = await this.$store.getters["auth/s3"].send(putCommand);
        const profilePicKey = `https://videogenesis-profilepics.s3.us-west-2.amazonaws.com/${putPayload.Key}`;

        this.$store.commit('users/rootUserSet', {
          ...this.user,
          profilePicKey: profilePicKey
        })

        await this.$store.dispatch("users/userPut", {
          profilePicKey: profilePicKey,
        });

      } catch (error) {
        console.error(error);
      }

      this.profilePictureLoading = false
    },
    async onBannerChange(file) {
      if (!this.isRootUser) return
      
      if (!file || !file.type) return

      const typeArr = file.type.split("/");
      this.bannerPictureLoading = true;

      try {
        const bucket = "videogenesis-profilepics"

        //  Delete old banner
        if (this.bannerSrc) {
          const urlArr = this.bannerSrc.split("/");
          const deleteKey = urlArr[urlArr.length - 1];

          const deletePayload = {
            Bucket: bucket,
            Key: deleteKey,
          };

          const deleteCommand = new DeleteObjectCommand(deletePayload);
          await this.$store.getters["auth/s3"].send(
            deleteCommand
          );
        }

        const putPayload = {
          Bucket: bucket,
          Key: nanoid() + `.${typeArr[typeArr.length - 1]}`,
          Body: file,
        };

        const putCommand = new PutObjectCommand(putPayload);
        const putResp = await this.$store.getters["auth/s3"].send(putCommand);
        const coverPicKey = `https://videogenesis-profilepics.s3.us-west-2.amazonaws.com/${putPayload.Key}`;

        this.$store.commit('users/rootUserSet', {
          ...this.user,
          coverPicKey: coverPicKey
        })

        await this.$store.dispatch("users/userPut", {
          coverPicKey: coverPicKey,
        });

      } catch (error) {
        console.error(error);
      }

      this.bannerPictureLoading = false;
    }
  }
};
</script>

<style></style>

