"""Business objects for the course structure API"""


class Structure(object):
    """
    The course structure object, which represents a tree of nodes.
    """
    def __init__(self, payload):
        self.payload = payload

    @property
    def blocks(self):
        """Returns all the blocks in the structure"""
        for block_id in self.payload['blocks'].keys():
            yield Block(block_id, self.payload)

    @property
    def _root_id(self):
        return self.payload['root']

    @property
    def root(self):
        """Returns the root node in the course"""
        root_id = self._root_id
        return Block(root_id, self.payload)

    def __str__(self):
        return 'Structure for {}'.format(self._root_id)


class Block(object):
    """
    Represents a single block within the course structure.
    """
    def __init__(self, block_id, json):
        self.json = json
        self.block_id = block_id

    def _get_block(self, block_id=None):
        if not block_id:
            block_id = self.block_id
        return self.json['blocks'][block_id]

    @property
    def children(self):
        """Returns blocks for each of this blocks children"""
        children = []
        for child in self._get_block()['children']:
            children.append(Block(child, self.json))
        return children

    @property
    def visible(self):
        """Returns whether the block is visible to non-staff"""
        # False, because if we're a non-staff user, we don't get the
        # visibile_to_staff_only field, it seems.
        return not self._get_block().get('visible_to_staff_only', False)

    @property
    def title(self):
        """Returns title"""
        return self._get_block()['display_name']

    def __str__(self):
        return self.block_id
