<template>
  <div class="flex flex-row items-center">
    <div
      v-if="user && !!user.profilePicKey"
      @click="openUserPage"
      style="width: 36px; height: 36px"
      class="mr-1"
    >
      <img
        :src="user.profilePicKey"
        :alt="user.username"
        class="rounded-full w-full h-full object-cover cursor-pointer"
      />
    </div>
    <v-icon v-else large class="mr-1" @click="openUserPage">icon-account-circle</v-icon>
    <div>
      <v-btn
        color="orange"
        plain
        @click="openUserPage"
        class="user-button px-0 text-left"
      >{{ user |  userDisplayName }}
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
      type: Object
    }
  },
  methods: {
    openUserPage() {
      this.$router.push(`/users/username=${this.user.pk.substr(3)}`);
    },
  }
}
</script>

<style scoped>
button.user-button >>> span.v-btn__content {
  align-items: flex-start;
}
</style>