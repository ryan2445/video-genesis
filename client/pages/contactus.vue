<template>
  <div>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css"
    />
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
      integrity="sha512-9usAa10IRO0HhonpyAIVpjrylPvoDwiPUiKdWk5t3PyolY1cOd4DSE0Ga+ri4AuTroPR5aQvXU9xC6qOPnzFeg=="
      crossorigin="anonymous"
      referrerpolicy="no-referrer"
    />
    <form
      ref="contact-us-form"
      @submit.prevent="SendEmail($event.currentTarget)"
    >
      <div class="field is-horizontal bg-gray-600">
        <div class="field-label is-normal">
          <label class="label">From</label>
        </div>
        <div class="field-body">
          <div class="field">
            <p class="control is-expanded has-icons-left">
              <input
                class="input"
                type="text"
                placeholder="Name"
                name="from_name"
              />
              <span class="icon is-small is-left">
                <i class="fas fa-user"></i>
              </span>
            </p>
          </div>
          <div class="field">
            <p class="control is-expanded has-icons-left has-icons-right">
              <input
                class="input"
                type="email"
                placeholder="Email"
                value=""
                name="from_email"
              />
              <span class="icon is-small is-left">
                <i class="fas fa-envelope"></i>
              </span>
              <!-- <span class="icon is-small is-right">
                <i class="fas fa-check"></i>
              </span> -->
            </p>
          </div>
        </div>
      </div>
      <div class="field is-horizontal">
        <div class="field-label"></div>
        <div class="field-body">
          <div class="field is-expanded">
            <div class="field has-addons">
              <p class="control">
                <a class="button is-static"> +1 </a>
              </p>
              <p class="control is-expanded">
                <input
                  class="input"
                  type="tel"
                  placeholder="Your phone number"
                  name="from_phone_number"
                />
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Country</label>
        </div>
        <div class="field-body">
          <div class="field is-narrow">
            <div class="control">
              <div class="select is-fullwidth">
                <select name="from_country">
                  <option>United States</option>
                  <option>Canada</option>
                  <option>China</option>
                  <option>India</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label">
          <label class="label">First Time User?</label>
        </div>
        <div class="field-body">
          <div class="field is-narrow">
            <div class="control">
              <label class="radio">
                <input type="radio" name="member" />
                Yes
              </label>
              <label class="radio">
                <input type="radio" name="member" />
                No
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Subject</label>
        </div>
        <div class="field-body">
          <div class="field">
            <div class="control">
              <input
                class="input"
                type="text"
                placeholder="e.g. Trouble Accessing Video"
                name="subject"
              />
            </div>
            <p class="help is-danger"></p>
          </div>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Question</label>
        </div>
        <div class="field-body">
          <div class="field">
            <div class="control">
              <textarea
                class="textarea"
                placeholder="how we can help you"
                name="message"
              ></textarea>
            </div>
          </div>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label"></div>
        <div class="field-body">
          <div class="field">
            <div class="control">
              <button type="submit" class="button is-primary">
                send message
              </button>
            </div>
          </div>
        </div>
      </div>
    </form>
    <div v-show="sendMessageSuccess">
      <br />
      <v-alert border="right" color="blue-grey" dark>
        Thank you for your message.
      </v-alert>
    </div>
  </div>
</template>
<script>
// emailjs
import emailjs from "@emailjs/browser";
export default {
  layout: "dashboard",
  created() {
    this.$store.commit("app/setRoute", "Contact Us");
  },
  data() {
    return {
      sendMessageSuccess: false,
    };
  },
  methods: {
    SendEmail(form) {
      emailjs
        .sendForm(
          "service_gbmy4bi",
          "template_mvv2l0u",
          // this.$refs["contact-us-form"],
          form,
          "user_b3vs3lNhdFhCw8CZDwjzj"
        )
        .then(
          (result) => {
            return new Promise((resolve, reject) => {
              // this.$refs["contact-us-form"].reset();
              form.reset();
              this.sendMessageSuccess = true;
              resolve();
            }).then(() => {
              setInterval(() => {
                this.sendMessageSuccess = false;
              }, 7000);
            });
          },
          (error) => {
            console.log("FAILED...", error.text);
          }
        );
    },
  },
};
</script>

<style scoped></style>
