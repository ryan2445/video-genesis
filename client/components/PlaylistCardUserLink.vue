<template>
  <div
    class="playlist-user"
  >
    <NuxtLink :to="`users/username=${user.pk.substr(3)}`">
      <h2
        class="text-xs text-gray-700"
      >
        {{ user | userDisplayName }}
      </h2>
    </NuxtLink>
  </div>
</template>

<script>
export default {
  name: "PlaylistCardUserLink",
  props: {
    user: {
      type: Object,
      required: true
    }
  }
}
</script>