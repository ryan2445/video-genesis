<template>
  <div class="flex flex-row items-center">
    <div
      v-if="showPic && user && !!user.profilePicKey"
      @click="openUserPage"
      style="width: 36px; height: 36px"
      class="mr-1"
    >
      <img
        v-if="user.profilePicKey"
        :src="user.profilePicKey"
        :alt="user.username"
        class="rounded-full w-full h-full object-cover cursor-pointer"
      />
      <v-icon v-else large class="mr-1" @click="openUserPage"
        >icon-account-circle</v-icon
      >
    </div>
    <div>
      <v-btn
        color="#A13440"
        plain
        @click.prevent="openUserPage"
        class="user-button px-0 text-left py-0"
        dense
      >
        <span :class="textClasses">
          {{ user | userDisplayName }}
        </span>
      </v-btn>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfilePictureAndUsername",
  props: {
    user: {
      required: true,
      type: Object,
    },
    showPic: {
      type: Boolean,
      required: false,
      default: true,
    },
    textClasses: {
      type: String,
      required: false,
      default: null,
    },
  },
  methods: {
    openUserPage() {
      this.$router.push(`/users/username=${this.user.pk.substr(3)}`);
    },
  },
};
</script>

<style scoped>
button.user-button >>> span.v-btn__content {
  align-items: flex-start;
}
</style>
