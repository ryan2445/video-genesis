<template>
  <div class="w-full relative pr-9">
    <v-btn
      v-if="hasPermission"
      absolute icon
      class="right-0 top-0"
      @click="() => !editMode ? handleEdit() : handleSave()"
    >
      <v-icon>
        {{ editMode ? 'mdi-content-save' : 'icon-pencil-outline'}}
      </v-icon>
    </v-btn>
    <p v-if="!editMode" class="text-base">
      {{ this.user.usersAboutMe }}
    </p>
    <v-textarea
      v-else
      rows="2"
      v-model="usersAboutMeCopy"
      color="orange"
    >

    </v-textarea>
  </div>
</template>

<script>
export default {
  name: "ProfileAbout",
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      editMode: false,
      usersAboutMeCopy: ''
    }
  },
  mounted() {
    this.usersAboutMeCopy = this.user.usersAboutMe;
  },
  methods: {
    handleEdit() {
      this.editMode = !this.editMode;

      
    },
    async handleSave() {
      const resp = await this.$store.dispatch('users/userPut', {
        ...this.user,
        usersAboutMe: this.usersAboutMeCopy
      })

      this.$store.commit("users/rootUserSet", {
        ...this.user,
        usersAboutMe: this.usersAboutMeCopy
      })

      this.editMode = false
    }
  },
  computed: {
    hasPermission() {
      return this.user.pk === this.$store.getters['users/rootUser'].pk
    }
  }
};
</script>

<style></style>
