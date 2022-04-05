<template>
  <div>
    <div class="h-20 flex mb-4 mt-2">
      <div class="p-2 mr-2">
        <img
          class="h-full w-full object-cover rounded-full"
          height="40"
          width="40"
          :src="user.profilePicKey"
          alt="avatar"
          style="border: solid 1px #e1e1e1"
        />
      </div>
      <!-- main -->
      <div class="flex flex-col">
        <!-- header -->
        <div>
          <h2 class="mt-3 font-semibold">{{ user.username }}</h2>
        </div>
        <div>{{ comment.content }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    comment: {
      type: Object,
      required: true,
    },
    user: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style></style>
