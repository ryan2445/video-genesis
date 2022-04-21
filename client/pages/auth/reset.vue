<template>
  <div class="flex flex-col content-center">
    <div class="flex flex-row justify-left items-center">
      <div class="w-3/4 fix-height">
        <img
          id="image0_29_21383"
          class="object-cover object-bottom w-full h-full"
          src="https://images.unsplash.com/photo-1625465004402-d16eb1e01960?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80"
        />
      </div>
      <div class="ml-5">
        <div v-if="!success">
          <h1>We've emailed a verification code to {{ toEmail }}</h1>
          <validation-provider
            name="Verification code"
            rules="required|numeric|length:6"
            v-slot="{ errors }"
          >
            <v-text-field
              id="resetCode"
              :error="!!errors"
              :error-messages="errors"
              placeholder="Code"
              :success="!errors"
              v-model="code"
            >
            </v-text-field>
          </validation-provider>
          <validation-provider
            name="Password"
            rules="required|min:8"
            v-slot="{ errors }"
          >
            <v-text-field
              id="passwordAuth"
              :error-messages="errors"
              placeholder="Password"
              :success="!errors"
              v-model="password"
              type="password"
              color="orange lighten-1"
            />
          </validation-provider>
          <v-btn
            @click="resetPassword()"
            :disabled="!password || !code"
            class="mt-3 white--text"
            color="orange lighten-1"
          >
            Submit
          </v-btn>
        </div>
        <div v-else>
          <h1>You're password has successfully been reset.</h1>
          <v-btn
            @click="$router.push('/auth/sign-in')"
            color="orange lighten-1"
            text
          >
            Click here to login
          </v-btn>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      username: null,
      code: null,
      password: null,
      success: false,
      toEmail: null,
    };
  },
  mounted() {
    this.username = this.$route.query.username;

    this.$auth
      .forgotPassword(this.username)
      .then((data) => {
        console.log("Reset Password Email Sent", data);
        this.toEmail = data.CodeDeliveryDetails.Destination;
      })
      .catch((err) => console.log(err));
  },
  methods: {
    resetPassword() {
      this.$auth
        .forgotPasswordSubmit(this.username, this.code, this.password)
        .then((data) => {
          if (data) this.success = true;
        })
        .catch((err) => console.log(err));
    },
  },
};
</script>

<style scoped>
.fix-height {
  height: 100vh;
}
</style>
