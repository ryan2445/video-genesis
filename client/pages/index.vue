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
export default {
    computed: {
        ...mapGetters({
            user: 'user/user'
        })
    }
}
</script>
