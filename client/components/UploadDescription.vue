<template>
  <div class="flex flex-col justify-center content-center bg-gray-200 p-10">
      <v-text-field 
        label="Title"
        v-model="title"
        @change="onChange"
      />
      <v-text-field
        label="Description"
        v-model="description"
        @change="onChange"
      />
    </div>
</template>

<script>
export default {
  name: "UploadDescription",
  data() {
    return {
      // The v-model bounded title
      title: null,

      // The v-model bounded description
      description: null,
    };
  },
  methods: {
    onChange() {
      this.$emit('update', {
        title: this.title,
        description: this.description
      })
    }
  }
};
</script>

<style scoped>
</style>