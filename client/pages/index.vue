<template>
    <div>
        <h1
            class="text-center"
        >
            Welcome to Video Genesis 😀
        </h1>

    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import AuthForm from '../components/AuthForm.vue'
export default {
  components: { AuthForm },
    computed: {
        ...mapGetters({
            user: 'user/user'
        })
    }
}
</script>
