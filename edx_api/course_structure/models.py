"""Business objects for the course structure API"""


class Structure(object):
    """
    The course structure object, which represents a tree of nodes.
    """
    def __init__(self, payload):
        self.payload = payload

    def blocks(self):
        """Returns all the blocks in the structure"""
        pass

    def root(self):
        """Returns the root node in the course"""
        root_id = self.payload['root']
        return Block(root_id, self.payload)


class Block(object):
    """
    Represents a single block within the course structure.
    """
    def __init__(self, block_id, json):
        self.json = json
        self.block_id = block_id

    def _get_block(self, block_id):
        return self.json['blocks'][block_id]

    def children(self):
        """Returns blocks for each of this blocks children"""
        children = []
        for child in self._get_block(self.block_id)['children']:
            children.append(self._get_block(child))
        return children

    def visible(self):
        """Returns whether the block is visible to non-staff"""
        return not self._get_block(self.block_id)['visible_to_staff_only']
