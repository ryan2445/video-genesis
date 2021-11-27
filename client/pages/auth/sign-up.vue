<template>
    <div class="flex flex-col">
        <h1> 
            Sign Up
        </h1>
        <AuthForm
            type="signUp"
            @signUp="onSignUp"
        />
        <NuxtLink to='/'>Home Page</NuxtLink>
    </div>
</template>

<script lang="js">
export default {
    name: "sign-up",
    methods: {
        onSignUp() {
            this.$router.push({
                path: '/auth/confirm'
            })
        }
    }
}
</script>
