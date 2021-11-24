<template>
    <div class="flex flex-col">
        <h1> {{ title }} </h1>
        <AuthForm
            v-if="step === 1 || step === 3"
            :type="authFormType"
            @signUp="setStep(2)"
            @signIn="setStep(4)"
        />
        <ConfirmAuthForm
            v-if="step === 2"
            @confirmed="setStep(3)"
        />
    </div>
</template>

<script lang="js">
export default {
    name: "Auth",
    data() {
        return {
            step: 1
        }
    },
    methods: {
        setStep(val) {
            this.step = val
        }
    },
    computed: {
        authFormType() {
            return this.step === 1
                ? 'signUp'
                : 'signIn'
        },
        title() {

            switch (this.step) {
                case 1:
                    return 'Sign Up'
                    break;
                case 2:
                    return 'Confirm'
                    break;
                case 3:
                    return 'Sign In'
                    break;
                case 4:
                    return 'Signed In!'
                default:
                    break;
            }
        }
    }
}
</script>