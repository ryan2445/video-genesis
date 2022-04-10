<template>
    <div class="d-flex my-4">
        <div class="" style="width:300px;">
            <v-text-field v-model="searchText" @input="search"
                prepend-inner-icon="mdi-magnify" placeholder="Search Videos..." rounded
                outlined dense hide-details color="orange" />
        </div>
    </div>
</template>
<script>
import { debounce } from 'lodash'
export default {
    data() {
        return {
            searchText: null
        }
    },
    methods: {
        search: debounce(function () {
            this.$emit('search', this.searchText)
        }, 500)
    }
}
</script>