"""Contract for checking the shape of newly added project packs."""


def template_shape(root):
    raise NotImplementedError


def shape_errors(folder, shape, root):
    raise NotImplementedError


def new_packs(base, root):
    raise NotImplementedError
