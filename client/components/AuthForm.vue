<template>
    <validation-observer ref="validationObservation" v-slot="{ invalid }">
        <v-form
            ref="signupForm"
            @submit.prevent="onSubmit"
        >
            <!-- Username Input -->
            <validation-provider
                name="username"
                rules="required|min:3"
                v-slot="{ errors }"
            >
                <v-text-field
                    id="usernameAuth"
                    :error="!!errors"
                    :error-messages="errors"
                    placeholder="Username"
                    :success="!errors"
                    v-model="username"
                >
                </v-text-field>
            </validation-provider>

            <!-- Email Input -->
            <validation-provider
                v-if="type === 'signUp'"
                name="email"
                rules="required|email"
                v-slot="{ errors }"
            >
                <v-text-field
                    id="emailAuth"
                    :error="!!errors"
                    :error-messages="errors"
                    placeholder="Email"
                    :success="!errors"
                    v-model="email"
                >
                </v-text-field>
            </validation-provider>

            <!-- Password Input -->
            <validation-provider
                name="password"
                rules="required|min:8"
                v-slot="{ errors }"
            >
                <v-text-field
                    id="passwordAuth"
                    :error="!!errors"
                    :error-messages="errors"
                    placeholder="Password"
                    :success="!errors"
                    v-model="password"
                    type="password"
                />
            </validation-provider>

            <!-- Submit Button -->
            <v-btn
                @click="onSubmit"
                :disabled="invalid"
            >
                Submit
            </v-btn>
        </v-form>
    </validation-observer>
</template>

<script lang="js">
export default {
    name: "AuthForm",
    props: {
        // Form Type: String - 'signUp' | 'signIn'
        type: {
            validator: function (value) {
                return ['signUp', 'signIn'].indexOf(value) !== -1
            },
            required: false,
            default: 'signUp'
        }
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
            loading: false
        }
    },
    computed: {

    },
    methods: {
        async onSubmit() {
            // If we are loading, return
            if (this.loading) return

            // Indicate that we are loading
            this.loading = true

            // Check if the form is valid
            const isValid = await this.$refs.validationObservation.validate()

            // If the form is not valid, return
            if (!isValid) {
                this.loading = false
                return
            }

            // Depending on the Auth type, sign up or sign in
            switch (this.type) {
                case 'signUp':
                    this.signUp();
                    break;
                case 'signIn':
                    this.signIn();
                    break;
                default:
                    break;
            }
        },

        async signUp() {
            // Create the request payload
            const request = {
                'username': this.username,
                'password': this.password,
                attributes: {
                    'email': this.email
                }
            }

            // Send a sign up request
            try {
                const { user } = await this.$auth.signUp(request)

                this.$store.commit('user/setUser', {
                    ...user,
                    'username': this.username,
                    'email': this.email
                })

                this.$emit('signUp')
            }
            catch (error) {
                console.log('error signing up:', error)
            }

            this.loading = false
        },

        async signIn() {
            // Send a sign in request
            try {
                const user = await this.$auth.signIn(this.username, this.password);

                this.$store.commit('user/setUser', {
                    ...user,
                    'username': this.username,
                })

                // Commit it
                this.$store.dispatch('auth/authorize', {
                    auth: this.$auth,
                    axios: this.$axios
                })

                this.$emit('signIn')
            }
            catch (error) {
                console.log('error signing in:', error)
            }
            
            this.loading = false
        }
    }
}
</script>