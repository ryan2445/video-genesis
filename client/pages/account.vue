<template>
  <section>
    <v-layout column align-center justify-center class="white--text">
      <h1
        class="text-xs-center orange--text mb-2 display-1"
        style="font-weight: 1000; text-shadow: 3px 2px #000000"
      >
        Account Settings
      </h1>
      <div clas="d-flex" style="text-align: center">
        <div class="font-weight-bold my-8">Account Settings</div>
        <div class="">Welcome</div>
        <div>
          {{ user && user.username }}
        </div>
      </div>
    </v-layout>
  </section>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  layout: "dashboard",
  computed: {
    ...mapGetters({
      user: "user/user",
    }),
  },
};
</script>
