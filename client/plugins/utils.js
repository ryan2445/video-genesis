export default({ app }, inject) => {
  const deserializeVideoData = (videos) => {
    videos = videos.map((video) => {
      if (video.videoData) {
        video.videoData = JSON.parse(video.videoData)
      }
      if (video.altThumbnails) {
        video.altThumbnails = JSON.parse(video.altThumbnails)
      }
      
      return video
    })
  
    return videos
  }

  inject('deserializeVideoData', deserializeVideoData)
}