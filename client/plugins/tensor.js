import { cast, browser, expandDims, loadGraphModel, tensor} from '@tensorflow/tfjs'

const Tensor = {
  preprocess: (image) => {
    // Load it with the new decodeImage Function
    const hr_image = browser.fromPixels(image)

    // change the type to 'float32' from 'int32'
    const castImage = cast(hr_image, 'float32')

    // expand the dims for multiple batch capabilities
    return expandDims(castImage, 0)
  },
  loadModel:  async () => {
    const modelUrl = 'https://model-weights-123.s3.us-west-2.amazonaws.com/srgan/model.json';
    return await loadGraphModel(modelUrl)
  },
  predict: (model, image) => {
    return model.predict(image)
  }
}

export default function ({ app }, inject) {
  inject("tensor", Tensor);
}