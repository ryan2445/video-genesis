<template>
  <div
    class="flex flex-col m-auto h-screen place-content-center text-center bg-gray-200"
  >
    <div
      class="p-7 place-self-center bg-white rounded-md"
      v-if="user"
      style="width: 360px"
    >
      <h1>Confirm Email</h1>
      <ConfirmAuthForm @confirmed="onConfirmed" />
    </div>
    <div v-else>
      <h1>No user found</h1>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  computed: {
    ...mapGetters({
      user: "users/rootUser",
    }),
  },
  methods: {
    onConfirmed() {
      this.$router.push({
        path: "/auth/sign-in",
      });
    },
  },
};
</script>
