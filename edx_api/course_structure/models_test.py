"""Model Tests"""
import os.path
import json
from unittest import TestCase

from .models import Structure, Block


class StructureTests(TestCase):
    """Tests for structure object"""
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/course_structure.json')) as file_obj:
            cls.structure = json.loads(file_obj.read())

        cls.subject = Structure(cls.structure)

    def test_root_obj(self):
        """gets root object"""
        assert self.subject.root.block_id == self.structure['root']

    def test_blocks(self):
        """blocks return iterable of blocks"""
        blocks = self.subject.blocks
        assert isinstance(next(blocks), Block)

    def test_str(self):
        """str test"""
        assert str(self.subject) == (
            "Structure for block-v1:edX+DemoX+Demo_Course+type"
            "@course+block@course"
        )


BLOCK_ID = (
    "block-v1:edX+DemoX+Demo_Course+type@chapter+block"
    "@1414ffd5143b4b508f739b563ab468b7"
)


class BlockTests(TestCase):
    """Tests for block object"""
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures/course_structure.json')) as file_obj:
            cls.structure = json.loads(file_obj.read())

    def test_children_length(self):
        """Children returns the correct number of blocks"""
        block = Block(BLOCK_ID, self.structure)
        assert len(block.children) == 1

    def test_visiblity(self):
        """Visible returns correct result"""
        block = Block(BLOCK_ID, self.structure)
        assert block.visible

    def test_title(self):
        """Title returns correct result"""
        block = Block(BLOCK_ID, self.structure)
        assert block.title == "About Exams and Certificates"

    def test_str(self):
        """str test"""
        block = Block(BLOCK_ID, self.structure)
        assert str(block) == BLOCK_ID
