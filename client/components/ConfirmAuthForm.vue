<template>
    <validation-observer ref="validationObservation" v-slot="{ invalid }">
        <v-form
            ref="confirmAuthForm"
            @submit.prevent="onSubmit"
        >
            <!-- Code Input -->
            <validation-provider
                name="username"
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
            <div class="flex flex-row">
                <v-btn
                    @click="onSubmit"
                    :disabled="invalid"
                >
                    Submit
                </v-btn>
                <v-btn
                    @click="onResend"
                >
                    Resend Code
                </v-btn>
            </div>
        </v-form>
    </validation-observer>
</template>

<script lang="js">
export default {
    name: "ConfirmAuthForm",
    props: {

    },
    data() {
        return {
            // The v-model value bounded to the code input
            code: null,

            // Flag that determines if the request is loading
            loading: false
        }
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

            this.confirmSignUp()
        },

        async confirmSignUp() {
            // Send a confirm sign up request
            try {
                await this.$auth.confirmSignUp(
                    this.$store.getters['user/user'].username,
                    this.code
                );

                this.$emit('confirmed')

                // Commit it
                this.$store.dispatch('auth/authorize', {
                    auth: this.$auth,
                    axios: this.$axios
                })
            }
            catch (error) {
                console.log('error confirming sign up', error)
            }
        },

        async onResend() {
            try {
                await this.$auth.resendSignUp(
                    this.$store.getters['user/user'].username
                )
            }
            catch (error) {
                console.log('error resending code:', error)
            }
        }
    },
    computed: {

    }
}
</script>