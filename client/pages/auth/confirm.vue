<template>
    <div class="flex flex-col">
        <h1> 
            Confirm Email
        </h1>
        <ConfirmAuthForm
            @confirmed="onConfirmed"
        />
    </div>
</template>

<script lang="js">
export default {
    name: "sign-up",
    methods: {
        onConfirmed() {
            this.$router.push({
                path: '/auth/sign-in'
            })
        }
    }
}
</script>
