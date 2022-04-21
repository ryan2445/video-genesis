<template>
  <validation-observer ref="validationObservation" v-slot="{ invalid }">
    <v-form ref="confirmAuthForm" @submit.prevent="onSubmit">
      <!-- Code Input -->
      <validation-provider
        name="Verification code"
        rules="required|numeric|length:6"
        v-slot="{ errors }"
      >
        <v-text-field
          id="confirmAuth"
          :error="!!errors"
          :error-messages="errors"
          placeholder="Code"
          :success="!errors"
          v-model="code"
        >
        </v-text-field>
      </validation-provider>

      <!-- Submit Button -->
      <div class="text-center">
        <div class="my-2">
          <v-btn
            @click="onSubmit"
            class="white--text"
            color="orange lighten-1"
            :disabled="invalid"
          >
            Submit
          </v-btn>
        </div>
        <div>
          <v-btn @click="onResend" small text> Resend Code </v-btn>
        </div>
      </div>
    </v-form>
  </validation-observer>
</template>

<script>
export default {
  data() {
    return {
      // The v-model value bounded to the code input
      code: null,

      // Flag that determines if the request is loading
      loading: false,
    };
  },
  methods: {
    async onSubmit() {
      // If we are loading, return
      if (this.loading) return;

      // Indicate that we are loading
      this.loading = true;

      // Check if the form is valid
      const isValid = await this.$refs.validationObservation.validate();

      // If the form is not valid, return
      if (!isValid) {
        this.loading = false;
        return;
      }

      this.confirmSignUp();
    },
    async confirmSignUp() {
      // Send a confirm sign up request
      try {
        const response = await this.$auth.confirmSignUp(
          this.$store.getters["users/rootUser"].username,
          this.code
        );

        this.$emit("confirmed");
      } catch (error) {
        console.log("error confirming sign up", error);
      }
    },
    async onResend() {
      try {
        await this.$auth.resendSignUp(
          this.$store.getters["users/rootUser"].username
        );
      } catch (error) {
        console.log("error resending code:", error);
      }
    },
  },
};
</script>
