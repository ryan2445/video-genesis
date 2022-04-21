<template>
  <div
    class="flex flex-col justify-center content-center bg-gray-200 px-10 py-4"
  >
    <validation-observer ref="validationObservation">
      <v-form ref="videoDescriptionForm">
        <validation-provider
          name="Title"
          rules="required|min:3|max:255"
          v-slot="{ errors }"
        >
          <v-text-field
            label="Title*"
            color="#A13440"
            :error-messages="errors"
            v-model="title"
            @change="onChange"
            filled
          />
        </validation-provider>
        <validation-provider
          name="Description"
          rules="max:1000"
          v-slot="{ errors }"
        >
          <v-textarea
            label="Description"
            v-model="description"
            color="#A13440"
            @change="onChange"
            :error-messages="errors"
            filled
          />
        </validation-provider>
        <v-container fluid>
          <v-checkbox
            v-model="isPrivate"
            label="Make the Video Private"
            color="#A13440"
            @change="onChange"
          ></v-checkbox>
        </v-container>
      </v-form>
    </validation-observer>
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
      isPrivate: false,
    };
  },
  methods: {
    onChange() {
      this.$emit("update", {
        title: this.title,
        description: this.description,
        isPrivate: this.isPrivate,
      });
    },
    resetUploadDescritpion() {
      (this.title = null), (this.description = null);
    },
  },
};
</script>

<style scoped></style>
