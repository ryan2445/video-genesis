<template>
  <div
    class="absolute top-0 left-0 z-30 transform -rotate-45 pt-1 pl-1 w-24 text-center -translate-x-6 translate-y-1 border-2 border-black border-solid"
    style="background: #ff9800a6;"
  >
    <v-tooltip top open-delay="300" nudge-bottom="30">
      <template v-slot:activator="{ on, attrs }">
        <div v-bind="attrs" v-on="on">
          <span class="text-white text-sm font-weight-bold select-none">SR+</span>
        </div>
      </template>
      <span>Super resolution enabled video</span>
    </v-tooltip>
  </div>
</template>

<script>
export default {
  name: "SuperResolutionBanner"
}
</script>