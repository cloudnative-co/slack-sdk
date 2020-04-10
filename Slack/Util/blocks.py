import copy
import uuid
import json
from collections import OrderedDict


class Blocks(object):

    blocks = OrderedDict()

    def append(self, block: dict):
        if "block_id" not in block:
            block["block_id"] = str(uuid.uuid4())
        block_id = block["block_id"]
        self.blocks[block_id] = block

    def load(self, blocks):
        for block in blocks:
            if "block_id" not in block:
                block["block_id"] = str(uuid.uuid4())
            block_id = block["block_id"]
            type = block["type"]
            if type == "actions":
                elements = OrderedDict()
                for element in block["elements"]:
                    if "action_id" not in element:
                        element["action_id"] = str(uuid.uuid4())
                    action_id = element["action_id"]
                    elements[action_id] = element
                block["elements"] = elements
            self.blocks[block_id] = block
            self.blocks.move_to_end(block_id)

    def has(self, block_id: str):
        return (block_id in self.blocks)

    def insert(self, prev_id: str, block: dict, is_next: bool = True):
        if "block_id" not in block:
            block["block_id"] = str(uuid.uuid4())
        block_id = block["block_id"]
        ids = list(self.blocks.keys())
        if prev_id not in ids:
            self.append(block)
            return
        if is_next:
            index = ids.index(prev_id) + 1
        else:
            index = ids.index(prev_id)
        blocks = list(self.blocks.items())
        blocks.insert(index, (block_id, block))
        self.blocks = OrderedDict(blocks)

    def set_select_value(self, action_id, option: dict):
        blocks = copy.deepcopy(self.blocks)
        for block_id, block in blocks.items():
            type = block["type"]
            if type == "section":
                if "accessory" not in block:
                    continue
                if block["accessory"]["action_id"] != action_id:
                    continue
                if block["accessory"]["type"] != "static_select":
                    continue
                if option not in block["accessory"]["options"]:
                    continue
                block["accessory"]["initial_option"] = option
                self.blocks[block_id] = block
                return True
            if type == "actions":
                if "elements" not in block:
                    continue
                if action_id not in block["elements"]:
                    continue
                if block["elements"][action_id]["type"] != "static_select":
                    continue
                if option not in block["elements"][action_id]["options"]:
                    continue
                block["elements"][action_id]["initial_option"] = option
                self.blocks[block_id] = block
                return True
        return False

    def append_select_field(self, block_id, text: str, index: int = None):
        if block_id not in self.blocks:
            return False
        type = self.blocks[block_id]["type"]
        if type != "section":
            return False
        if "fields" not in self.blocks[block_id]:
            self.blocks[block_id]["fields"] = list()
        if index is not None:
            count = len(self.blocks[block_id]["fields"])
            if count > index:
                self.blocks[block_id]["fields"][index] = {
                    "type": "mrkdwn",
                    "text": text
                }
                return True
        self.blocks[block_id]["fields"].append({
            "type": "mrkdwn",
            "text": text
        })
        return True

    def get_value(self, action_id):
        for block_id, block in self.blocks.items():
            type = block["type"]
            if type == "section":
                if "accessory" not in block:
                    continue
                if block["accessory"]["action_id"] != action_id:
                    continue
                if block["accessory"]["type"] == "static_select":
                    return block["accessory"]["initial_option"]["value"]
                elif block["accessory"]["type"] == "datepicker":
                    return block["accessory"]["initial_date"]
            if type == "actions":
                if "elements" not in block:
                    continue
                if action_id not in block["elements"]:
                    continue
                element = block["elements"][action_id]
                if element["type"] == "static_select":
                    return element["initial_option"]["value"]
                elif element["type"] == "datepicker":
                    return element["initial_date"]
        return None

    def get_values(self):
        result = {}
        for block_id, block in self.blocks.items():
            type = block["type"]
            if type == "section":
                if "accessory" not in block:
                    continue
                action_id = block["accessory"]["action_id"]
                if block["accessory"]["type"] == "static_select":
                    if "initial_option" not in block["accessory"]:
                        result[action_id] = None
                        continue
                    value = block["accessory"]["initial_option"]["value"]
                    result[action_id] = value
                elif block["accessory"]["type"] == "datepicker":
                    if "initial_date" not in block["accessory"]:
                        result[action_id] = None
                        continue
                    result[action_id] = block["accessory"]["initial_date"]
            if type == "actions":
                if "elements" not in block:
                    continue
                for action_id, element in block["elements"].items():
                    if element["type"] == "static_select":
                        if "initial_option" not in element:
                            result[action_id] = None
                            continue
                        result[action_id] = element["initial_option"]["value"]
                    elif element["type"] == "datepicker":
                        if "initial_date" not in element:
                            result[action_id] = None
                            continue
                        result[action_id] = element["initial_date"]
        return result

    def set_datepicker(self, action_id, value):
        blocks = copy.deepcopy(self.blocks)
        for block_id, block in blocks.items():
            type = block["type"]
            if type == "section":
                if "accessory" not in block:
                    continue
                if block["accessory"]["action_id"] != action_id:
                    continue
                if block["accessory"]["type"] != "datepicker":
                    continue
                block["accessory"]["initial_date"] = value
                self.blocks[block_id] = block
                return True
            if type == "actions":
                if "elements" not in block:
                    continue
                if action_id not in block["elements"]:
                    continue
                if block["elements"][action_id]["type"] != "datepicker":
                    continue
                block["elements"][action_id]["initial_date"] = value
                self.blocks[block_id] = block
                return True
        return False

    def delete(self, block_id):
        if block_id in self.blocks:
            del self.blocks[block_id]

    def list(self):
        result = list()
        blocks = copy.deepcopy(self.blocks)
        for block_id, block in blocks.items():
            if "elements" in block:
                block["elements"] = list(block["elements"].values())
            result.append(block)
        return result

    def add_actions(self, block_id: str):
        self.blocks[block_id] = {
            "type": "actions",
            "block_id": block_id,
            "elements": OrderedDict()
        }

    def insert_actions(
        self,
        prev_id: str,
        block_id: str,
        is_next: bool = True
    ):
        block = {
            "type": "actions",
            "block_id": block_id,
            "elements": OrderedDict()
        }
        self.insert(prev_id, block, is_next)

    def append_action(self, block_id: str, block: dict):
        if "action_id" not in block:
            block["action_id"] = str(uuid.uuid4())
        action_id = block["action_id"]
        self.blocks[block_id]["elements"][action_id] = block

    def set_actions(self, actions: list):
        for action in actions:
            type = action["type"]
            action_id = action["action_id"]
            if type == "static_select":
                value = action["selected_option"]
                self.set_select_value(action_id, value)
            if type == "datepicker":
                value = action["selected_date"]
                self.set_datepicker(action_id, value)
