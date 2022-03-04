<template>
  <div class="relative">
    <!-- This is the cover image for the banner -->
    <div
      v-if="userCoverPic"
      class="absolute bottom-0 h-56 overflow-hidden flex-1 justify-center items-center"
    >
      <img
        class="min-w-full min-h-full object-cover"
        :src="userCoverPic"
        alt="bird"
      />
    </div>
    <div
      v-if="userProfilePic"
      class="-bottom-16 left-14 absolute w-44 h-44 rounded-full overflow-hidden"
    >
      <img
        class="min-w-full min-h-full object-cover"
        :src="userProfilePic"
        alt="avatar"
      />
    </div>
  <div><button @click="Debug">debug</button></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      profilepic: null,
      coverpic: null,
    };
  },
  computed: {
    userProfilePic() {
      if (!this.user) return null;
      return this.profilepic || this.user[0]?.profilePicKey || "https://www.unr.edu/main/images/divisions/president/marketing-communications/brand/brand-athletics-2.png";
    },
    userCoverPic() {
      if (!this.user) return null;
      return this.coverpic || this.user[0]?.coverPicKey || "https://www.unr.edu/main/images/top-6/visit/components/campus-360.jpg";
    },
  },
  props: {
    user: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style></style>
