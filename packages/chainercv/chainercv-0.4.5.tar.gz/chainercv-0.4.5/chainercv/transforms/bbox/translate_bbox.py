def translate_bbox(bbox, x_offset=0, y_offset=0):
    """Translate bounding boxes.

    This method is mainly used together with image transforms, such as padding
    and cropping, which translates the left top point of the image from
    coordinate :math:`(0, 0)` to coordinate :math:`(x\_offset, y\_offset)`.

    The bounding boxes are expected to be packed into a two dimensional
    tensor of shape :math:`(R, 4)`, where :math:`R` is the number of
    bounding boxes in the image. The second axis represents attributes of
    the bounding box. They are :obj:`(x_min, y_min, x_max, y_max)`,
    where the four attributes are coordinates of the bottom left and the
    top right vertices.

    Args:
        bbox (~numpy.ndarray): Bounding boxes to be transformed. The shape is
            :math:`(R, 4)`. :math:`R` is the number of bounding boxes.
        x_offset (int or float): The offset along x axis.
        y_offset (int or float): The offset along y axis.

    Returns:
        ~numpy.ndarray:
        Bounding boxes translated according to the given offsets.

    """

    out_bbox = bbox.copy()
    out_bbox[:, :2] += (x_offset, y_offset)
    out_bbox[:, 2:] += (x_offset, y_offset)

    return out_bbox
