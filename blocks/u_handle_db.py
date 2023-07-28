import os
import json


def read_db_cell(cell, subcell=None, deepsubcell=None, filename='s_main_db.json'):
    with open(f'./data/{filename}', 'r', encoding='utf-8') as f:
        data = json.load(f)
        if subcell is None:
            return data[cell]
        elif deepsubcell is None:
            return data[cell][subcell]
        else:
            return data[cell][subcell][deepsubcell]
        # read_db_cell("cell", "subcell"/+"deepsubcell", "filename")


def write_db_cell(cell, value, subcell=None, deepsubcell=None, filename="s_main_db.json"):
    with open(f'data/{filename}', 'r+', encoding='utf-8') as f:
        data = json.load(f)
        if subcell is None:
            data[cell] = value
        elif deepsubcell is None:
            data[cell][subcell] = value
        else:
            data[cell][subcell][deepsubcell] = value
        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.truncate()
        # write_db_cell("cell", значение, "subcell", "filename")


# def add_line_db(cell, subcell, value, filename="s_main_db.json"):
#     data = read_db_cell(cell, filename=filename)
#     data[subcell] = value
#     write_db_cell(cell, data, filename=filename)


def clear_db(filename='s_main_db.json'):
    filepath = os.path.join('resource', 'data', filename)
    with open(filepath, 'w') as f:
        json.dump({}, f)
