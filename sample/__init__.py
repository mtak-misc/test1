from pythonforandroid.recipe import RustCompiledComponentsRecipe


class OrjsonRecipe(RustCompiledComponentsRecipe):
    version = "3.10.4"
    url = "https://github.com/ijl/orjson/archive/refs/tags/{version}.tar.gz"
    use_maturin = True
    hostpython_prerequisites = ["typing_extensions"]
    site_packages_name = "orjson"


recipe = OrjsonRecipe()
