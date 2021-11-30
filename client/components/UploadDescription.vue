<template>
  <div class="flex flex-col justify-center content-center bg-gray-200 p-10">
      <p>
        <strong>Upload</strong>
      </p>
       <p>
        <strong>Details</strong>
      </p>
       <p>
        <strong>Title(Required)</strong>
      </p>
      <v-text-field placeholder="Placeholder Text">
                </v-text-field>

        <p>
        <strong>Description</strong>
      </p>
      <v-text-field placeholder="What is your video about">
                </v-text-field>
      <v-container>
          
    <v-row>
      <v-col col="12">
        <v-combobox
          v-model="select"
          :items="items"
          label="Select Category"
          multiple
        ></v-combobox>
      </v-col>
    </v-row>
  </v-container>
    <p>
        <strong>Thumbnail</strong>
      </p>
  <div>
      <input type="file" id="upload-file" class="upload-file" />
    </div>
    </div>
  
</template>

<script>
export default {
  name: "HelloWorld",
  data() {
    return {
      
      items: ["Music", "Funny", "inspirational", "Sports"],
    };
  },
};
</script>

<style scoped>
</style>