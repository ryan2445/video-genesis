<template>
  <v-container>
<!--
      <v-card
      v-for="({title, username, description}) in data" :key="title"
      class="mx-auto"
      outlined
    >
    <v-list-item three-line>
      <v-list-item-content>
          <v-img
            height="250"
            src="https://cdn.vuetifyjs.com/images/cards/cooking.png"
          ></v-img>
        <div class="text-overline mb-4">
          {{title}}
        </div>
        <v-list-item-title class="text-h5 mb-1">
          {{username}}
        </v-list-item-title>
        <v-list-item-subtitle>{{description}}</v-list-item-subtitle>
      </v-list-item-content>

    </v-list-item>


  </v-card>

  -->

  <br /> <br /> <br /> 

      <div v-for="({title, username, description}) in data" :key="title"> 
      <v-card
        class="mx-auto"
        outlined
      >
        <v-row>
          <v-col cols="4">
                  
            <v-img
              height="250"
              src="https://cdn.vuetifyjs.com/images/cards/cooking.png"
            ></v-img>
          </v-col>
          <v-col cols="8">
            

            <v-list-item three-line>
              <v-list-item-content>
                <div class="text-overline mb-4">
                  {{title}}
                </div>
                <v-list-item-title class="text-h5 mb-1">
                  {{username}}
                </v-list-item-title>
                <v-list-item-subtitle>{{description}}</v-list-item-subtitle>
              </v-list-item-content>

            </v-list-item>
          </v-col>
        </v-row>

      </v-card>
      <br /> 
    </div>
  </v-container>
</template>
 
<script>
export default {
  name: "VideoCard",

  props: [],

  data() {
    return {
      data: [],
    };
  },
  created() {
    this.data = 
    [
      {
        title: "fake title", 
        username: "fake username", 
        description: "fake discription"
      }, 
      {
        title: "fake title1", 
        username: "fake username1", 
        description: "fake discription1"
      }, 
      {
        title: "fake title2222", 
        username: "fake username2222", 
        description: "fake discriptio2222n"
      }
    ]
  },
};
</script>
 
<style></style>