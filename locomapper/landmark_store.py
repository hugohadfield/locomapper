import json
from typing import Dict, Tuple
from pathlib import Path

from pydantic import BaseModel


class LandmarkStore:
    """ Store for landmark data. """
    def __init__(self, data_model: BaseModel):
        """ Initialize the LandmarkStore with a data model."""
        self.data_model: BaseModel = data_model
        self._storage: Dict[int, Tuple[BaseModel, ...]] = {}

    def get(self, identifier: str) -> Tuple[BaseModel, ...]:
        """ Get the data for a given identifier."""
        return self._storage.get(identifier, ())

    def put(self, datum: BaseModel) -> bool:
        """ Put the data into the store."""
        identifier = datum.identifier
        found_data_flag = False
        if identifier in self._storage:
            existing_data = self._storage[identifier]
            self._storage[identifier] = existing_data + (datum,)
            found_data_flag = True
        else:
            self._storage[identifier] = (datum,)
        return found_data_flag

    def __len__(self) -> int:
        """ Return the number of elements in the store."""
        return len(self._storage)

    def save(self, save_file: str):
        """ Save the store to a json file."""
        save_path = Path(save_file).absolute()
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert each tuple of BaseModels into a list of dicts
        serializable_data = {
            str(identifier): [model.dict() for model in models_tuple]
            for identifier, models_tuple in self._storage.items()
        }

        with open(save_path, "w", encoding="utf-8") as file:
            json.dump(serializable_data, file, indent=2)

    def load(self, load_file: str) -> int:
        """ Load the store from a json file. Returns the number of identifiers loaded."""
        load_path = Path(load_file).absolute()
        with open(load_path, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        # Rebuild the dictionary of tuples of BaseModels
        self._storage = {
            identifier: tuple(self.data_model(**model_dict) for model_dict in models_list)
            for identifier, models_list in raw_data.items()
        }
        return len(self._storage)
