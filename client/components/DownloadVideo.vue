<template>
  <v-menu offset-y v-model="menuDisplay">
    <template v-slot:activator="{ on, attrs }"> 
      <v-btn 
        v-bind="attrs" v-on="on" 
        icon
        :loading="downloading"
        :disabled="downloading"
      >
      <v-icon>
        mdi-download
      </v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        Downloads
      </v-card-title>
      <v-divider></v-divider>
      <v-list>
        <v-list-item
          v-for="link of downloadLinks"
          :key="link.url"
        >
          <a
            @click="download(link)"
          >
            {{ link.title }}
          </a>
        </v-list-item>
      </v-list>
    </v-card>
  </v-menu>
</template>

<script>
export default {
  name: "DownloadVideo",
  props: {
    video: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      menuDisplay: false,
      BUCKET_URL: "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
      downloading: false
    }
  },
  methods: {
    download(link) {
      if (this.downloading) return

      const url = link.url
      const filename = link.title

      this.downloading = true

      try {
        fetch(url)
          .then(resp => resp.blob())
          .then(blob => {
            this.downloading = false

            const blobURL = URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = blobURL;
            a.style = "display: none;"


            document.body.appendChild(a)
            a.click()
          })
      }
      catch(e) {
        this.$notify({
          text: 'Download error, try again'
        })
      }
      finally {
        this.downloading = false
      }
    }
  },
  computed: {
    downloadLinks() {
      const links = this.video.videoData.map(data => {
        return {
          url: `${this.BUCKET_URL}/${this.video.videoKey}/${data.baseURL}`,
          title: data.width
        }
      })

      links.push({
        url: `${this.BUCKET_URL}/${this.video.videoKey}/${this.video.videoKey}.mp4`,
        title: 'audio'
      })

      if (!!this.video.lrBaseURL) {
        links.push({
          url: `${this.BUCKET_URL}/${this.video.videoKey}/${this.video.lrBaseURL}`,
          title: 'DS'
        })
      }
      if (!!this.video.hrBaseURL) {
        links.push({
          url: `${this.BUCKET_URL}/${this.video.videoKey}/${this.video.hrBaseURL}`,

          title: 'SR'
        })
      }

      return links
    }
  }
}
</script>