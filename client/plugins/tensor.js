import { Tensor3D, cast, node, expandDims, clipByValue, Tensor4D, loadGraphModel, io, GraphModel} from '@tensorflow/tfjs-node'

const Tensor = {
  preprocess = (path) => {
    //get image
    const image = fs.readFileSync(path)

    //load it with the new decodeImage Function
    const hr_image = node.decodeImage(new Uint8Array(image), 3)

    //change the type to 'float32' from 'int32'
    const castImage = cast(hr_image, 'float32')

    // expand the dims for multiple batch capabilities
    return expandDims(castImage, 0)
  },
  loadModel = async () => {
    return await loadGraphModel(io.fileSystem('./weights/srgan/model.json'))
  },
  predict = (model) => {
    
  }
}