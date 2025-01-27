<template>
  <v-card
    elevation="0"
    style="padding: 14px 12px"
    min-width="360px"
    class="relative"
  >
    <v-progress-linear
      absolute
      top
      indeterminate
      rounded
      :active="loading"
      color="#A13440"
    />
    <v-card-title class="justify-center">
      <h3
        v-text="`Sign ${type === 'signUp' ? 'up' : 'in'} for Video Genesis`"
      />
    </v-card-title>
    <v-card-text class="text-center">
      <validation-observer ref="validationObservation" v-slot="{ invalid }">
        <v-form ref="signupForm" @submit.prevent="onSubmit">
          <!-- Username Input -->
          <validation-provider
            name="Username"
            rules="required|min:3"
            v-slot="{ errors }"
          >
            <v-text-field
              id="usernameAuth"
              :error-messages="errors"
              placeholder="Username"
              :success="!errors"
              v-model="username"
              color="#A13440"
            >
            </v-text-field>
          </validation-provider>

          <!-- Email Input -->
          <validation-provider
            v-if="type === 'signUp'"
            name="Email"
            rules="required|email"
            v-slot="{ errors }"
          >
            <v-text-field
              id="emailAuth"
              :error-messages="errors"
              placeholder="Email"
              :success="!errors"
              v-model="email"
              @keydown.enter="onSubmit"
              color="#A13440"
            >
            </v-text-field>
          </validation-provider>

          <!-- Password Input -->
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
              @keydown.enter="onSubmit"
              color="#A13440"
            />
          </validation-provider>

          <!-- Forgot username / password options (only shown on signup page) -->
          <div v-if="type == 'signIn'">
            <v-btn x-small text color="blue lighten-1" @click="resetPassword()">
              Forgot your password?
            </v-btn>
          </div>

          <!-- Submit Button -->
          <v-btn
            @click="onSubmit"
            :disabled="invalid"
            class="mt-3 white--text"
            color="#A13440"
          >
            Submit
          </v-btn>
        </v-form>
      </validation-observer>
    </v-card-text>
    <v-dialog v-model="dialog" max-width="300">
      <v-card>
        <v-card-title class="text-h5">
          {{ dialogTitle }}
        </v-card-title>
        <v-card-text>
          {{ dialogText }}
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn color="#A13440" text @click="dialog = false"> Ok </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
export default {
  name: "AuthForm",
  props: {
    // Form Type: String - 'signUp' | 'signIn'
    type: {
      validator: function (value) {
        return ["signUp", "signIn"].indexOf(value) !== -1;
      },
      required: false,
      default: "signUp",
    },
  },
  data() {
    return {
      // The v-model value bounded to the username input
      username: null,
      // The v-model value bounded to the email input
      email: null,
      // The v-model value bounded to the password input
      password: null,
      // Flag that determines if the request is loading
      loading: false,
      dialogText: null,
      dialogTitle: null,
      dialog: null,
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

      // Depending on the Auth type, sign up or sign in
      switch (this.type) {
        case "signUp":
          this.signUp();
          break;
        case "signIn":
          this.signIn();
          break;
        default:
          break;
      }
    },

    async signUp() {
      // Create the request payload
      const request = {
        username: this.username,
        password: this.password,
        attributes: {
          email: this.email,
          // usersFirstName: "",
          // usersLastName: "",
          // usersAboutMe: "",
        },
      };

      // Send a sign up request
      try {
        const { user } = await this.$auth.signUp(request);

        this.$store.commit("users/rootUserSet", {
          ...user,
          username: this.username,
          email: this.email,
        });

        this.$emit("signUp");
      } catch (error) {
        switch (error.name) {
          case "UsernameExistsException":
            this.dialogTitle = "Signup Error";
            this.dialogText = "That username already exists";
            this.dialog = true;
        }
      }

      this.loading = false;
    },
    async signIn() {
      // Send a sign in request
      try {
        const user = await this.$auth.signIn(this.username, this.password);

        if (!user) return;

        this.$store.commit("auth/setToken", user.signInUserSession);

        await this.$store.dispatch("users/userGet");

        this.$emit("signIn");
      } catch (error) {
        this.dialogTitle = "Signin Error";
        this.dialogText = "That username or password is incorrect";
        this.dialog = true;
      }

      this.loading = false;
    },
    resetPassword() {
      this.$router.push({
        path: "/auth/reset",
        query: { username: this.username },
      });
    },
  },
};
</script>
