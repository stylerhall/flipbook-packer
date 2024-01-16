from pathlib import Path

__all__: list[str] = ["resources_dir"]


# the location of the resources folder, this is where
# example frames live
resources_dir: Path = Path(__file__).parents[2].joinpath("resources")

