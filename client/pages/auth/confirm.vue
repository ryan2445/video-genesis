<template>
  <div class="flex flex-col m-auto text-center" style="width: 360px">
    <div v-if="user">
      <h1>Confirm Email</h1>
      <ConfirmAuthForm @confirmed="onConfirmed" />
    </div>
    <div v-else>
      <h1>No user found</h1>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
export default {
  computed: {
    ...mapGetters({
      user: "user/user"
    })
  },
  methods: {
    onConfirmed() {
      this.$router.push({
        path: "/auth/sign-in"
      })
    }
  }
}
</script>
