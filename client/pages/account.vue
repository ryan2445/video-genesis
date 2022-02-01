<template>
    <div clas="d-flex" style="text-align:center;">
        <div class="font-weight-bold my-8">
            Account Settings
        </div>
        <div class="">
            Username:
        </div>
        <div>
            {{ user && user.username }}
        </div>
    </div>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
    layout: 'dashboard',
    computed: {
        ...mapGetters({
            user: 'user/user'
        })
    }
}
</script>
