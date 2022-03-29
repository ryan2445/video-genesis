<template>
    <div class="flex flex-col">
        <div class="flex justify-center">
            <svg width="952" height="800" viewBox="0 0 952 1024" fill="none"
                xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink">
                <rect width="1000" height="1036" fill="#FFF2E8" />
                <rect width="1000" height="1036" fill="url(#pattern0)" />
                <defs>
                    <pattern id="pattern0" patternContentUnits="objectBoundingBox"
                        width="1" height="1">
                        <use xlink:href="#image0_48_6220"
                            transform="translate(-0.316373) scale(0.000788005)" />
                    </pattern>
                    <image id="image0_48_6220" width="2072" height="1381"
                        xlink:href="https://images.unsplash.com/photo-1625465004402-d16eb1e01960?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" />
                </defs>
            </svg>
            <div v-if="!success">
                <h1>We've emailed a verification code to {{ toEmail }}</h1>
                <validation-provider name="Verification code"
                    rules="required|numeric|length:6" v-slot="{ errors }">
                    <v-text-field id="resetCode" :error="!!errors"
                        :error-messages="errors" placeholder="Code" :success="!errors"
                        v-model="code">
                    </v-text-field>
                </validation-provider>
                <validation-provider name="Password" rules="required|min:8"
                    v-slot="{ errors }">
                    <v-text-field id="passwordAuth" :error-messages="errors"
                        placeholder="Password" :success="!errors" v-model="password"
                        type="password" color="orange lighten-1" />
                </validation-provider>
                <v-btn @click="resetPassword()" :disabled="!password || !code"
                    class="mt-3 white--text" color="orange lighten-1">
                    Submit
                </v-btn>
            </div>
            <div v-else>
                <h1>You're password has successfully been reset.</h1>
                <v-btn @click="$router.push('/auth/sign-in')" color="orange lighten-1"
                    text>
                    Click here to login
                </v-btn>
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
            toEmail: null
        }
    },
    mounted() {
        this.username = this.$route.query.username

        this.$auth
            .forgotPassword(this.username)
            .then((data) => {
                console.log('Reset Password Email Sent', data)
                this.toEmail = data.CodeDeliveryDetails.Destination
            })
            .catch((err) => console.log(err))
    },
    methods: {
        resetPassword() {
            this.$auth
                .forgotPasswordSubmit(this.username, this.code, this.password)
                .then((data) => {
                    if (data) this.success = true
                })
                .catch((err) => console.log(err))
        }
    }
}
</script>
