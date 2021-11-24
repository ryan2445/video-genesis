<template>
    <div class="flex flex-col">
        <h1> 
            Sign In 
        </h1>
        <AuthForm
            type="signIn"
            @signIn="onSignIn"
        />
    </div>
</template>

<script lang="js">
export default {
    name: "sign-up",
    methods: {
        onSignIn() {
            this.$router.push({
                path: '/'
            })
        }
    }
}
</script>
