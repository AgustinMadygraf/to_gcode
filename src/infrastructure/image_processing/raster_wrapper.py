from typing import Any, Callable, cast
from skimage import io
from skimage.morphology import skeletonize  # type: ignore[reportUnknownVariableType]
from skimage.color import rgb2gray  # type: ignore[reportUnknownVariableType]
from skimage.filters import threshold_otsu  # type: ignore[reportUnknownVariableType]
import io as pyio
from src.adaptadores.pasarelas.envoltorios_tecnicos import AbstraccionEsqueleto, ImagenParecida, ProcesadorImagenRaster

class ScikitImageWrapper(ProcesadorImagenRaster):
    def __init__(self, skeleton_wrapper_factory: Callable[[Any], AbstraccionEsqueleto]):
        self._factory = skeleton_wrapper_factory

    def procesar_imagen_a_esqueleto(self, bytes_imagen: bytes) -> AbstraccionEsqueleto:
        """
        Processes image bytes into a skeletonized binary representation.
        Assumes dark lines on light background.
        """
        # Load image from bytes
        # Using ImagenParecida protocol to satisfy Pylance
        raw_image: ImagenParecida = cast(ImagenParecida, io.imread(pyio.BytesIO(bytes_imagen)))  # type: ignore[reportUnknownMemberType]
        
        # Convert to grayscale if it's RGB/RGBA
        if len(raw_image.shape) == 3:
            # Drop alpha channel if present
            if raw_image.shape[2] == 4:
                image: Any = raw_image[:, :, :3]
            else:
                image = raw_image
            gray: Any = cast(Any, rgb2gray(image))
        else:
            gray = raw_image
            
        # Thresholding (Binarization)
        # Assuming dark lines on light background, we want lines to be True (1)
        # Otsu's thresholding
        thresh: float = float(threshold_otsu(gray))
        binary: Any = gray < thresh 
        
        # Skeletonization
        skeleton: Any = cast(Any, skeletonize(binary))  # type: ignore[reportUnknownMemberType]
        
        return self._factory(skeleton)
